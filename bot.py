from __future__ import annotations

import asyncio
import base64
import hashlib
import html
import ipaddress
import json
import os
import re
import shutil
import signal
import tarfile
import time
import socket
import subprocess
import sys
import traceback
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional
from types import SimpleNamespace
from collections import OrderedDict
from datetime import datetime

import discord
from discord.ext import commands

ROOT = Path(__file__).resolve().parent
DEOB_DIR = ROOT / "deobf"
DEOB_SCRIPT = DEOB_DIR / "deob.py"
PYTHON = os.getenv("PYTHON", sys.executable or "python3")
MAX_INPUT_BYTES = max(1, int(os.getenv("MAX_INPUT_BYTES", str(8 * 1024 * 1024))))
MAX_OUTPUT_BYTES = max(1, int(os.getenv("MAX_OUTPUT_BYTES", str(24 * 1024 * 1024))))
JOB_TIMEOUT = max(10, min(1800, int(os.getenv("DEOB_TIMEOUT", "900"))))  # 15 min headroom for ~2 MB files
MAX_CONCURRENT_JOBS = max(1, int(os.getenv("MAX_CONCURRENT_JOBS", "2")))
URL_TIMEOUT = max(5, min(180, int(os.getenv("URL_TIMEOUT", "60"))))
ALLOWED_EXTENSIONS = {".lua", ".luau", ".txt"}
SUPPORTED = {
    "luraph_v15": {"label": "Luraph v15", "command": ".lrph15"},
    "luraph_v151": {"label": "Luraph v15.1", "command": ".lrph15.1"},
    "ironbrew1": {"label": "IronBrew1", "command": ".iron"},
    "moonsec_v3": {"label": "MoonSec V3", "command": ".moon"},
    "centurion": {"label": "Centurion", "command": ".cent"},
}

V151_DIR = DEOB_DIR / "v151"
V151_SCRIPT = V151_DIR / "deob.js"
V151_NODE_ARCHIVE = V151_DIR / "vendor" / "node-v20.19.5-linux-x64.tar.gz"
V151_NODE_DIRNAME = "node-v20.19.5-linux-x64"
_node_bin: Optional[str] = None


def resolve_node() -> str:
    """Path to a node binary: system node if present, else the vendored runtime."""
    global _node_bin
    if _node_bin:
        return _node_bin
    found = shutil.which("node")
    if found:
        _node_bin = found
        return _node_bin
    if not V151_NODE_ARCHIVE.is_file():
        raise RuntimeError("vendored node runtime archive is missing")
    target = Path(tempfile.gettempdir()) / "monlua-node"
    node_exe = target / V151_NODE_DIRNAME / "bin" / "node"
    if not node_exe.is_file():
        target.mkdir(parents=True, exist_ok=True)
        try:
            with tarfile.open(V151_NODE_ARCHIVE, "r:gz") as archive:
                archive.extractall(target, filter="data")
        except TypeError:
            with tarfile.open(V151_NODE_ARCHIVE, "r:gz") as archive:
                archive.extractall(target)
    if not node_exe.is_file():
        raise RuntimeError("could not unpack the vendored node runtime")
    node_exe.chmod(0o755)
    _node_bin = str(node_exe)
    return _node_bin

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
job_slots = asyncio.Semaphore(MAX_CONCURRENT_JOBS)

# Render's free instance has 512 MiB total for everything. A deobfuscation job
# that runs past this budget is stopped (with a clear error card) instead of
# letting the container OOM-kill the whole service and leave the user's
# "Devirtualizing..." message hanging forever. The budget is shared across the
# concurrent jobs MAX_CONCURRENT_JOBS allows.
JOB_MEM_BUDGET_MB = 330
_active_jobs = 0

# Free cloud runner: big jobs are dispatched to the private GitHub Actions
# repo in GH_JOBS_REPO (a runner has ~8 GB RAM and 2 dedicated cores), so big
# files finish in a couple of minutes instead of exhausting the 512 MB
# Render instance. Small files keep running locally; any cloud failure falls
# back to the local engine. Identical re-runs are answered instantly from
# _RESULT_CACHE.
GH_JOBS_REPO = os.getenv("GH_JOBS_REPO", "yarhm0962/monlua-jobs")
GH_DISPATCH_TOKEN = os.getenv("GH_DISPATCH_TOKEN", "")
CLOUD_V151_MIN_BYTES = 150_000
CLOUD_OTHER_MIN_BYTES = 1_000_000
CLOUD_WAIT_SECONDS = 1500
CLOUD_POLL_SECONDS = 8
cloud_slots = asyncio.Semaphore(1)
_RESULT_CACHE: OrderedDict = OrderedDict()
_RESULT_CACHE_BYTES = 0
_RESULT_CACHE_MAX_BYTES = 32 * 1024 * 1024


class _LoggedLayoutView(discord.ui.LayoutView):
    """Surface component errors in the logs instead of swallowing them."""

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print(f"View error for {item} in {type(self).__name__}: {error!r}\n{traceback.format_exc()}", flush=True)


def info_view(title: str, body: str, color: int = 0x5865F2) -> discord.ui.LayoutView:
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=color)
    container.add_item(discord.ui.TextDisplay(f"## {title}"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(body.strip()))
    view.add_item(container)
    return view


def engines_body() -> str:
    return (
        "**SUPPORTED ENGINES**\n"
        "• **Luraph v15.1** · `.lrph15.1`\n"
        "• **Luraph v15** · `.lrph15`\n"
        "• **IronBrew 1** · `.iron`\n"
        "• **MoonSec V3** · `.moon`\n"
        "• **Centurion** · `.cent`\n\n"
        "**HOW TO START**\n"
        "Attach one `.lua`, `.luau`, or `.txt` file, or provide a direct raw-file URL.\n"
        "Run `.detect` first, then use the matching engine command.\n\n"
        "**QUICK COMMANDS**\n"
        "• `.detect` — identify an obfuscator\n"
        "• `.get <url>` — fetch raw text\n"
        "• `.help` — show this guide"
    )


def _human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


def _strip_lua_comments(source: str) -> str:
    """Remove Lua/Luau comments without touching quoted or long-bracket strings."""
    out = []
    i, n = 0, len(source)
    marker = "-- [[ Deobfuscated by MonLua ]]"
    while i < n:
        if source.startswith("--", i):
            line_start = source.rfind("\n", 0, i) + 1
            line_end = source.find("\n", i)
            if line_end < 0:
                line_end = n
            if source[line_start:i].strip() == "" and source[i:line_end].strip() == marker:
                i = line_end + (1 if line_end < n else 0)
                continue
            long_comment = re.match(r"--\[(=*)\[", source[i:])
            if long_comment:
                close = "]" + long_comment.group(1) + "]"
                end = source.find(close, i + long_comment.end())
                end = n if end < 0 else end + len(close)
                out.append("\n" * source[i:end].count("\n"))
                i = end
            else:
                out.append("\n" if line_end < n else "")
                i = line_end + (1 if line_end < n else 0)
            continue
        if source[i] == '"' or source[i] == "'" or source[i] == chr(96):
            quote = source[i]
            start = i
            i += 1
            while i < n:
                if source[i] == "\\":
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            out.append(source[start:i])
            continue
        if source[i] == "[":
            long_string = re.match(r"\[(=*)\[", source[i:])
            if long_string:
                close = "]" + long_string.group(1) + "]"
                start = i
                end = source.find(close, i + long_string.end())
                i = n if end < 0 else end + len(close)
                out.append(source[start:i])
                continue
        out.append(source[i])
        i += 1
    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", "".join(out)).strip()


def _beautify_lua(source: str) -> str:
    """Use StyLua when installed; otherwise use the bundled Luau token formatter."""
    body = source.strip()
    if not body:
        return ""
    stylua = shutil.which("stylua")
    if stylua:
        try:
            proc = subprocess.run(
                [stylua, "--stdin-filepath", "output.luau", "-"],
                input=body, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=20, check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    try:
        from deobf.lexer import pretty, tokenize
        formatted = pretty(tokenize(body), max_str=len(body) + 1).strip()
        if formatted:
            return formatted
    except Exception as exc:
        print(f"Lua formatter fallback: {type(exc).__name__}: {exc}", flush=True)
    return body


def _prepare_deobfuscated_output(source: str) -> str:
    """Enforce one MonLua header, remove all other comments, and beautify code."""
    body = _strip_lua_comments(source.lstrip("\ufeff"))
    formatted = _beautify_lua(body)
    return "-- [[ Deobfuscated by MonLua ]]\n\n" + formatted.rstrip() + "\n"


PASTEFY_API_URL = "https://pastefy.app/api/v2/paste"
PASTEFY_TOKEN = os.getenv("PASTEFY_TOKEN", "").strip()
PASTEFY_API_URL = "https://pastefy.app/api/v2/paste"
PASTEFY_TOKEN = os.getenv("PASTEFY_TOKEN", "").strip()
PASTEFY_CHUNK_CHARS = 450_000   # per paste; stays under Pastefy's ~1 MB request cap even with JSON escaping


def _pastefy_post(payload: dict):
    headers = {"Content-Type": "application/json"}
    attempts = ([{"Authorization": PASTEFY_TOKEN}] if PASTEFY_TOKEN else []) + [{}]
    for auth in attempts:
        try:
            request = urllib.request.Request(
                PASTEFY_API_URL, data=json.dumps(payload).encode("utf-8"),
                headers={**headers, **auth})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8", errors="replace"))
            paste = data.get("paste") or {}
            if paste.get("id"):
                return paste
            print(f"Pastefy upload rejected: {str(data)[:200]}", flush=True)
        except Exception as exc:
            print(f"Pastefy upload failed ({'with token' if auth else 'anonymous'}): {type(exc).__name__}: {exc}", flush=True)
    return None


def _pastefy_upload(text: str, title: str) -> str:
    """Upload output to Pastefy; outputs past the ~1 MB per-paste cap are split into
    numbered parts with an index paste holding every link. Returns the paste URL or ""."""
    if not text:
        return ""
    chunks = [text[i:i + PASTEFY_CHUNK_CHARS] for i in range(0, len(text), PASTEFY_CHUNK_CHARS)]
    urls = []
    for i, chunk in enumerate(chunks, 1):
        part_title = title[:110] if len(chunks) == 1 else f"{title[:96]} ({i}/{len(chunks)})"
        paste = _pastefy_post({"content": chunk, "title": part_title})
        if not paste:
            return ""
        urls.append(f"https://pastefy.app/{paste['id']}")
    if len(urls) == 1:
        return urls[0]
    index = _pastefy_post({
        "content": "Full output split across Pastefy parts (in order):\n\n"
                   + "\n".join(f"Part {i}: {u}" for i, u in enumerate(urls, 1)),
        "title": f"{title[:96]} - index"})
    if index:
        return f"https://pastefy.app/{index['id']}"
    return urls[0]


def result_view(filename: str, label: str, size: int, code_text, file_name, elapsed: str = "", pastefy_url: str = "") -> discord.ui.LayoutView:
    """Create a compact result card with a clear hierarchy on narrow screens."""
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=0x57F287)
    container.add_item(discord.ui.TextDisplay("## ✅ Deobfuscation complete"))
    summary = f"**Engine**  {label}\n**Output size**  {_human_size(size)}"
    if elapsed:
        summary += f"\n**Time**  {elapsed}"
    container.add_item(discord.ui.TextDisplay(summary))
    container.add_item(discord.ui.TextDisplay(f"-# File: `{filename[:180]}`"))
    container.add_item(discord.ui.Separator())
    if code_text is not None:
        container.add_item(discord.ui.TextDisplay(f"```lua\n{code_text}\n```"))
    if file_name is not None:
        container.add_item(discord.ui.File(discord.UnfurledMediaItem(f"attachment://{file_name}")))
        container.add_item(discord.ui.TextDisplay("📎 **Output file attached**\n-# Download the attachment to save the full result."))
    if pastefy_url:
        container.add_item(discord.ui.TextDisplay(
            f"**Online copy**\n[Open Pastefy]({pastefy_url}) · [View raw text]({pastefy_url}/raw)"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay("-# Review the output before running it."))
    view.add_item(container)
    return view


def error_view(title: str, detail: str) -> discord.ui.LayoutView:
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=0xED4245)
    container.add_item(discord.ui.TextDisplay(f"## ⚠️ {title}"))
    container.add_item(discord.ui.TextDisplay("The job could not finish. Review the details below, then try again if appropriate."))
    container.add_item(discord.ui.Separator())
    safe_detail = str(detail or "No diagnostic details were provided.").strip()[-900:]
    safe_detail = safe_detail.replace("```", "`\u200b``")
    container.add_item(discord.ui.TextDisplay(f"```text\n{safe_detail}\n```"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay("**Next step**  Run `.detect` to identify the engine, or `.help` for usage."))
    view.add_item(container)
    return view


DETECT_HEADER_HINTS = ("luraph", "moonsec", "ironbrew")


def detect_view(filename: str, rows, basis: str, elapsed: str = "", source=None) -> discord.ui.LayoutView:
    """Report card for `.detect`: every engine scored against the file, with
    the concrete signals each score came from. `source` enables the one-click
    Deobfuscate button when the best match is 100% on a supported engine."""
    rows = [(n, c, l, e) for n, c, l, e in rows if n != "generic"]
    general = next(((c, l, e) for n, c, l, e in rows if n in ("obfuscated", "plain")), None)
    engines = [(n, c, l, e) for n, c, l, e in rows if n not in ("obfuscated", "plain")]
    best_name, best_conf, best_label, best_ev = engines[0] if engines else ("", 0.0, "", [])
    matched = best_conf >= 0.75
    partial = 0.30 <= best_conf < 0.75
    if matched:
        color, title = 0x57F287, "## \U0001f50d Obfuscator identified"
    elif partial:
        color, title = 0xFAA61A, "## \U0001f50d Possible match"
    elif general and general[0] >= 0.5:
        color, title = 0xFAA61A, "## \U0001f50d Obfuscated, engine not supported"
    elif general:
        color, title = 0x5865F2, "## \u2139\ufe0f No obfuscation detected"
    else:
        color, title = 0xED4245, "## \u2753 Unknown obfuscator"
    one_click = None
    if source is not None and matched and best_conf >= 0.999 and best_name in SUPPORTED:
        one_click = (best_name, source)
    view = _LoggedLayoutView()
    if one_click:
        view.timeout = None          # keep the button usable for the process lifetime
    container = discord.ui.Container(accent_color=color)
    container.add_item(discord.ui.TextDisplay(title))
    head = f"-# `{filename}`"
    if elapsed:
        head += f" \u00b7 \u23f1\ufe0f {elapsed}"
    container.add_item(discord.ui.TextDisplay(head))
    container.add_item(discord.ui.Separator())
    if matched or partial:
        verdict = "Identified" if matched else "Likely"
        detection_only = best_name not in ("luraph_v15", "luraph_v151", "ironbrew1", "moonsec_v3")
        note = " \u00b7 detection only" if detection_only else ""
        container.add_item(discord.ui.TextDisplay(
            f"**{verdict}:** {best_label} \u00b7 **{int(round(best_conf * 100))}%** confidence{note}"
        ))
        others = [(l, c) for n, c, l, e in engines[1:] if c > 0]
        ev = best_ev
    elif general and general[0] >= 0.5:
        container.add_item(discord.ui.TextDisplay(
            f"Obfuscated ({int(round(general[0] * 100))}% structural match), "
            "but no supported engine or known family fits.\n"
            "Likely a custom or private obfuscator."
        ))
        others = [(l, c) for n, c, l, e in engines if c > 0]
        ev = general[2]
    elif general:
        container.add_item(discord.ui.TextDisplay(
            "This script looks **unobfuscated** \u2014 no engine or known obfuscator family matched it."
        ))
        others = []
        ev = []
    else:
        container.add_item(discord.ui.TextDisplay(
            "No engine reached the 75% confidence threshold."
        ))
        others = [(l, c) for n, c, l, e in engines if c > 0]
        ev = []
    details = [f"Matched by {basis}"]
    if others:
        others_text = " \u00b7 ".join(f"{lab} ({int(round(c * 100))}%)" for lab, c in others[:3])
        details.append(f"Also considered: {others_text}")
    if ev:
        shown = " \u00b7 ".join(str(x) for x in ev[:3] if str(x))
        details.append(f"Signals: {shown}")
    container.add_item(discord.ui.TextDisplay("\n".join(f"-# {d}" for d in details)))
    stats = ("\u2699\ufe0f Button below deobfuscates with this engine" if one_click
             else "\U0001f4a1 `.detect` identifies only \u2014 run the engine's command to deobfuscate")
    container.add_item(discord.ui.TextDisplay(f"-# {stats}"))
    if one_click:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.ActionRow(_DeobfuscateButton(*one_click)))
    view.add_item(container)
    return view


class _DetectInvoker:
    """Stands in for commands.Context so the .detect button can reuse process_input."""

    def __init__(self, channel):
        self.channel = channel
        self.message = SimpleNamespace(attachments=[])

    async def reply(self, content=None, view=None, file=None, mention_author=False):
        return await self.channel.send(content, view=view, file=file)


class _DeobfuscateButton(discord.ui.Button):
    """The one-click run button on a 100%-confidence .detect report."""

    def __init__(self, engine: str, source: tuple):
        super().__init__(label="Deobfuscate", emoji="\u2699\ufe0f",
                         style=discord.ButtonStyle.success, custom_id="deobf_run")
        self._engine = engine
        self._source = source

    async def callback(self, interaction: discord.Interaction) -> None:
        try:
            view = _ConfirmDeobfView(self._engine, self._source, interaction.message, self.view)
        except Exception:
            print(f"Deobfuscate button: confirm view failed:\n{traceback.format_exc()}", flush=True)
            view = None
        label = SUPPORTED[self._engine]["label"]
        if view is None:
            await interaction.response.send_message(
                "\u26a0\ufe0f Couldn't open the confirmation card. Use the engine command directly (`.help`).",
                ephemeral=True)
            return
        src_name = self._source[1] if self._source[0] == "attachment" else "the linked file"
        await interaction.response.send_message(f"Deobfuscate `{src_name}` with **{label}**?", view=view)


class _ConfirmDeobfView(discord.ui.View):
    def __init__(self, engine: str, source: tuple, detect_message=None, detect_layout=None):
        super().__init__(timeout=None)
        self._engine = engine
        self._source = source
        self._detect_message = detect_message
        self._detect_layout = detect_layout
        self.add_item(_ConfirmDeobfButton(engine, source))
        self.add_item(_CancelDeobfButton())

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print(f"Confirm view error for {item}: {error!r}\n{traceback.format_exc()}", flush=True)


class _ConfirmDeobfButton(discord.ui.Button):
    def __init__(self, engine: str, source: tuple):
        super().__init__(label="Continue", style=discord.ButtonStyle.success, custom_id="deobf_confirm")
        self._engine = engine
        self._source = source

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        try:
            await interaction.message.delete()
        except discord.HTTPException:
            print(f"Confirm card delete failed:\n{traceback.format_exc()}", flush=True)
        # the one-click run is spent: grey out the Deobfuscate button on the report card
        detect_message = getattr(self.view, "_detect_message", None)
        detect_layout = getattr(self.view, "_detect_layout", None)
        if detect_message is not None and detect_layout is not None:
            try:
                for item in detect_layout.walk_children():
                    if isinstance(item, discord.ui.Button) and item.custom_id == "deobf_run":
                        item.disabled = True
                await detect_message.edit(view=detect_layout)
            except Exception:
                print(f"Detect button disable failed:\n{traceback.format_exc()}", flush=True)
        engine, source = self._engine, self._source
        url = source[1] if source[0] == "url" else ""
        preset = (source[1], source[2]) if source[0] == "attachment" else None
        invoker = _DetectInvoker(interaction.channel)
        try:
            await process_input(invoker, engine, url=url, preset=preset)
        except Exception as exc:
            print(f"Deobfuscate button job failed: {type(exc).__name__}: {exc}", flush=True)
            try:
                await interaction.channel.send(
                    view=error_view("Something went wrong", str(exc)[:400] or "Unknown error."))
            except discord.HTTPException:
                pass


class _CancelDeobfButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Cancel", style=discord.ButtonStyle.secondary, custom_id="deobf_cancel")

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(
            content="\ud83d\uddf1\ufe0f Cancelled \u2014 no job was started.", view=None)


@bot.listen("on_interaction")
async def _log_component_clicks(interaction: discord.Interaction) -> None:
    """Every button click is logged, so a dead interaction is never silent."""
    if interaction.type is not discord.InteractionType.component:
        return
    data = interaction.data or {}
    print(f"component-click: custom_id={data.get('custom_id')} "
          f"message={getattr(interaction.message, 'id', None)}", flush=True)


def runtime_status() -> tuple[bool, str]:
    suffix = ".exe" if os.name == "nt" else ""
    required = (DEOB_DIR / "bin" / f"luau{suffix}", DEOB_DIR / "bin" / f"luau-ast{suffix}", DEOB_SCRIPT)
    missing = [str(p) for p in required if not p.is_file() or (os.name != "nt" and not os.access(p, os.X_OK))]
    return (not missing, ", ".join(missing) if missing else ", ".join(map(str, required)))


def _validate_public_url(url: str, allow_any_ext: bool = False) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url.strip().strip("<>"))
    if parsed.scheme not in ("https", "http") or not parsed.hostname:
        raise ValueError("Please provide a direct HTTP(S) raw-file URL.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing embedded credentials are not accepted.")
    filename = Path(urllib.parse.unquote(parsed.path)).name
    suffix = Path(filename).suffix.lower()
    if not filename or (suffix and suffix not in ALLOWED_EXTENSIONS):
        if not allow_any_ext:
            raise ValueError("The raw URL must point directly to a `.lua`, `.luau`, or `.txt` file.")
    if suffix not in ALLOWED_EXTENSIONS:
        filename = "paste.lua"
    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
    except OSError as exc:
        raise ValueError("Could not resolve the URL host.") from exc
    for item in addresses:
        ip = ipaddress.ip_address(item[4][0].split("%", 1)[0])
        if not ip.is_global:
            raise ValueError("That URL host is not a publicly routable address.")
    return parsed.geturl(), filename


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
_BOT_UA = "DeobfuscatorDiscordBot/1.0"


def _extract_code_from_page(body: bytes) -> Optional[bytes]:
    """A paste/view page instead of raw code: dig the script out of it."""
    text = body.decode("utf-8", errors="replace")
    candidates = []
    for match in re.findall(
        r"<(?:pre|code|textarea)(?:\s[^>]*)?>(.*?)</(?:pre|code|textarea)>",
        text, re.IGNORECASE | re.DOTALL,
    ):
        candidates.append(html.unescape(match).strip("\r\n"))
    for key in ("content", "code", "source", "sourceCode", "data"):
        for chunk in re.findall(r'"%s"\s*:\s*"((?:[^"\\]|\\.)*)"' % key, text):
            try:
                candidates.append(json.loads('"%s"' % chunk))
            except ValueError:
                pass
    candidates = [item for item in candidates if item.strip()]
    if not candidates:
        return None
    return max(candidates, key=len).encode("utf-8")


def _download_url(url: str, destination: Path, allow_any_ext: bool = False) -> tuple[str, int]:
    current_url = url
    last_net_error: Optional[Exception] = None
    opener = urllib.request.build_opener(_NoRedirect)
    for attempt in range(2):          # one retry for transient network drops
        if attempt:
            time.sleep(2)             # brief backoff, then the same ladder again
        for _ in range(4):
            current_url, filename = _validate_public_url(current_url, allow_any_ext=allow_any_ext)
            response = None
            refused: Optional[urllib.error.HTTPError] = None
            for agent in (_BROWSER_UA, _BOT_UA):
                request = urllib.request.Request(current_url, headers={
                    "User-Agent": agent,
                    "Accept": "text/html,application/xhtml+xml,text/plain,application/octet-stream,*/*",
                    "Accept-Language": "en-US,en;q=0.9",
                })
                try:
                    response = opener.open(request, timeout=URL_TIMEOUT)
                    break
                except urllib.error.HTTPError as exc:
                    if exc.code in (301, 302, 303, 307, 308):
                        # Redirects are chased hop by hop at the top of the loop,
                        # so every new host still goes through _validate_public_url.
                        location = (exc.headers.get("Location") or "").strip()
                        if not location:
                            raise ValueError(
                                f"Could not download the raw file (HTTP {exc.code} with no redirect target)."
                            ) from exc
                        current_url = urllib.parse.urljoin(current_url, location)
                        break          # response/refused stay empty: hop loop retries the new URL
                    refused = exc
                    if exc.code in (401, 403, 406, 418, 429):
                        continue
                    raise ValueError(f"Could not download the raw file (HTTP {exc.code}).") from exc
                except (urllib.error.URLError, TimeoutError, OSError) as exc:
                    last_net_error = exc
                    continue
            if response is None:
                if refused is None:
                    continue          # both user agents hit network errors: retry via the outer loop
                code = refused.code
                raise ValueError(
                    f"Could not download the raw file (HTTP {code}). The host refuses automated downloads; "
                    "attach the file directly in Discord instead."
                )
            with response:
                final_url = response.geturl()
                if final_url != current_url:
                    _validate_public_url(final_url)
                content_type = response.headers.get_content_type().lower()
                declared = response.headers.get("Content-Length")
                if declared and int(declared) > MAX_INPUT_BYTES:
                    raise ValueError(f"File exceeds the {MAX_INPUT_BYTES:,}-byte input limit.")
                body = b""
                while True:
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break
                    body += chunk
                    if len(body) > MAX_INPUT_BYTES:
                        raise ValueError(f"File exceeds the {MAX_INPUT_BYTES:,}-byte input limit.")
                if content_type in {"text/html", "application/xhtml+xml"}:
                    extracted = _extract_code_from_page(body)
                    if extracted is None:
                        raise ValueError("That link returned a web page with no script code inside it. Use a direct raw link.")
                    body = extracted
                if not body:
                    raise ValueError("The source file is empty.")
                destination.write_bytes(body)
                return filename, len(body)
    if last_net_error is not None:
        raise ValueError("Could not download that raw URL even after a retry. Make sure it is publicly accessible.")
    raise ValueError("Too many redirects while downloading the raw file.")


async def _scan_engine(source_path: Path) -> tuple[Optional[str], str]:
    try:
        proc = await asyncio.create_subprocess_exec(
            PYTHON, str(DEOB_SCRIPT), str(source_path), "--detect", "--no-pypy",
            cwd=str(DEOB_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90)
    except asyncio.TimeoutError:
        return None, "The source scan timed out."
    except OSError as exc:
        return None, f"Could not start the source scanner: {exc}"
    output = stdout.decode("utf-8", errors="replace").strip()
    if proc.returncode != 0 or not output:
        detail = stderr.decode("utf-8", errors="replace").strip()
        return None, detail[-700:] or "The source scanner could not identify this script."
    parts = output.split("\t", 2)
    if len(parts) < 3:
        return None, "The scanner returned an unrecognized result."
    engine_name, confidence_text, _label = parts
    try:
        confidence = float(confidence_text) if confidence_text != "forced" else 1.0
    except ValueError:
        confidence = 0.0
    if engine_name not in SUPPORTED or confidence < 0.75:
        return None, f"Detected engine: {engine_name}; confidence: {confidence:.2f}."
    return engine_name, f"Detected {SUPPORTED[engine_name]['label']} (confidence {confidence:.2f})."


async def _detect_scores(source_path: Path) -> tuple[list[tuple[str, float, str, list[str]]], str]:
    """Score every engine against the file:
    [(name, confidence, label, evidence), ...], best first."""
    try:
        proc = await asyncio.create_subprocess_exec(
            PYTHON, str(DEOB_SCRIPT), str(source_path), "--detect-all", "--no-pypy",
            cwd=str(DEOB_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90)
    except asyncio.TimeoutError:
        raise ValueError("The detection scan timed out.")
    except OSError as exc:
        raise ValueError(f"Could not start the detection scan: {exc}")
    if proc.returncode != 0:
        detail = stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"The detection scan failed: {detail[-300:] or 'no diagnostic output'}")
    rows: list[tuple[str, float, str, list[str]]] = []
    for line in stdout.decode("utf-8", errors="replace").splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        try:
            evidence = parts[3].split(" | ") if len(parts) > 3 and parts[3].strip() else []
            rows.append((parts[0], float(parts[1]), parts[2], evidence))
        except ValueError:
            continue
    if not rows:
        raise ValueError("The detection scan returned no results.")
    try:
        head = source_path.read_bytes()[:600].decode("utf-8", errors="replace").lower()
    except OSError:
        head = ""
    if any(h in head for h in DETECT_HEADER_HINTS):
        basis = "header signature + full-file code structure"
    else:
        basis = "full-file code-structure analysis (no header comment)"
    return rows, basis


class JobMemoryExceeded(Exception):
    pass


def _self_rss_mb() -> int:
    try:
        with open("/proc/self/status") as fh:
            for line in fh:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) // 1024
    except OSError:
        pass
    return 0


def _tree_rss_kb(pgid: int) -> int:
    """Total resident memory of every process in the process group, in KiB."""
    total = 0
    try:
        entries = os.listdir("/proc")
    except OSError:
        return 0
    for entry in entries:
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/stat", "rb") as fh:
                tail = fh.read().rsplit(b")", 1)[1].split()
            if int(tail[2]) != pgid:  # after comm: state, ppid, pgrp
                continue
            with open(f"/proc/{entry}/status") as fh:
                for line in fh:
                    if line.startswith("VmRSS:"):
                        total += int(line.split()[1])
                        break
        except (OSError, ValueError, IndexError):
            continue
    return total


async def _run_process(args: list[str], timeout: int) -> tuple[int, bytes, bytes]:
    global _active_jobs
    proc = await asyncio.create_subprocess_exec(
        *args, cwd=str(DEOB_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
    )
    try:
        pgid = os.getpgid(proc.pid)
    except ProcessLookupError:
        pgid = proc.pid
    ceiling_mb = 0
    if JOB_MEM_BUDGET_MB:
        _active_jobs += 1
        ceiling_mb = max(160, JOB_MEM_BUDGET_MB // _active_jobs)
    mem_peak_kb = 0
    mem_exceeded = False

    async def _watch_memory() -> None:
        nonlocal mem_peak_kb, mem_exceeded
        while proc.returncode is None:
            await asyncio.sleep(0.5)
            rss = _tree_rss_kb(pgid)
            if rss > mem_peak_kb:
                mem_peak_kb = rss
            if ceiling_mb and rss > ceiling_mb * 1024:
                mem_exceeded = True
                print(f"Memory ceiling hit ({rss // 1024} MB > {ceiling_mb} MB), stopping the job tree", flush=True)
                try:
                    os.killpg(pgid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    watcher = asyncio.ensure_future(_watch_memory()) if ceiling_mb else None
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        if proc.returncode is None:
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        await proc.communicate()
        raise
    finally:
        if ceiling_mb:
            _active_jobs -= 1
        if watcher:
            watcher.cancel()
            try:
                await watcher
            except (asyncio.CancelledError, Exception):
                pass
    if mem_exceeded:
        raise JobMemoryExceeded(f"it peaked around {max(1, mem_peak_kb // 1024)} MB")
    return proc.returncode or 0, stdout, stderr


def _gh_time(value: str) -> float:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def _gh_api(method: str, path: str, *, body=None, accept: str = "application/vnd.github+json") -> tuple[int, bytes]:
    """One GitHub REST call. Returns (status, response bytes); HTTP errors are data."""
    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": accept,
        "Authorization": f"Bearer {GH_DISPATCH_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "monlua-bot",
    })
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _cloud_upload_input(job_id: str, data: bytes) -> None:
    body = {"message": f"input {job_id}", "content": base64.b64encode(data).decode("ascii")}
    code, resp = _gh_api("PUT", f"/repos/{GH_JOBS_REPO}/contents/jobs/{job_id}.input", body=body)
    if code not in (200, 201):
        raise RuntimeError(f"input upload failed: HTTP {code}: {resp[:200]!r}")


def _cloud_dispatch(engine: str, job_id: str) -> None:
    code, resp = _gh_api(
        "POST", f"/repos/{GH_JOBS_REPO}/actions/workflows/deobf.yml/dispatches",
        body={"ref": "main", "inputs": {"engine": engine, "job_id": job_id}})
    if code != 204:
        raise RuntimeError(f"dispatch failed: HTTP {code}: {resp[:200]!r}")


def _cloud_fetch_result(job_id: str) -> bytes:
    code, out = _gh_api(
        "GET", f"/repos/{GH_JOBS_REPO}/contents/results/{job_id}.luau?ref=result/{job_id}",
        accept="application/vnd.github.raw")
    if code == 200 and out:
        return out
    # large outputs: read the blob directly
    code2, meta = _gh_api("GET", f"/repos/{GH_JOBS_REPO}/contents/results/{job_id}.luau?ref=result/{job_id}")
    if code2 == 200:
        try:
            sha = json.loads(meta.decode("utf-8", errors="replace")).get("sha", "")
        except ValueError:
            sha = ""
        if sha:
            code3, blob = _gh_api("GET", f"/repos/{GH_JOBS_REPO}/git/blobs/{sha}")
            if code3 == 200:
                try:
                    return base64.b64decode(json.loads(blob.decode("utf-8", errors="replace"))["content"])
                except (ValueError, KeyError):
                    pass
    raise RuntimeError(f"result fetch failed: HTTP {code}")


def _cloud_cleanup(job_id: str) -> None:
    try:
        code, meta = _gh_api("GET", f"/repos/{GH_JOBS_REPO}/contents/jobs/{job_id}.input?ref=main")
        if code == 200:
            sha = json.loads(meta.decode("utf-8", errors="replace")).get("sha", "")
            if sha:
                _gh_api("DELETE", f"/repos/{GH_JOBS_REPO}/contents/jobs/{job_id}.input",
                        body={"message": f"cleanup {job_id}", "sha": sha})
    except Exception:
        pass
    _gh_api("DELETE", f"/repos/{GH_JOBS_REPO}/git/refs/heads/result/{job_id}")


def _cloud_deobfuscate(engine: str, input_path: Path, wait_seconds: int) -> bytes:
    """Run one deobfuscation job on the free GitHub Actions runner."""
    if not GH_DISPATCH_TOKEN:
        raise RuntimeError("no GitHub token configured")
    job_id = os.urandom(6).hex()
    _cloud_upload_input(job_id, input_path.read_bytes())
    _cloud_dispatch(engine, job_id)
    started_unix = time.time()
    deadline = started_unix + wait_seconds
    conclusion = None
    while time.time() < deadline:
        code, resp = _gh_api("GET", f"/repos/{GH_JOBS_REPO}/actions/runs?event=workflow_dispatch&per_page=15")
        if code == 200:
            try:
                runs = json.loads(resp.decode("utf-8", errors="replace")).get("workflow_runs") or []
            except ValueError:
                runs = []
            for run in runs:
                if run.get("head_branch") != "main":
                    continue
                if _gh_time(run.get("created_at", "")) < started_unix - 5:
                    continue
                if run.get("status") == "completed":
                    conclusion = run.get("conclusion") or "unknown"
                    break
        if conclusion is not None:
            break
        time.sleep(CLOUD_POLL_SECONDS)
    if conclusion is None:
        raise RuntimeError("the cloud runner did not answer in time")
    if conclusion != "success":
        raise RuntimeError(f"cloud run {conclusion}")
    out = _cloud_fetch_result(job_id)
    _cloud_cleanup(job_id)
    return out


def _cache_key(engine: str, input_path: Path) -> tuple[str, str]:
    try:
        digest = hashlib.sha256()
        with open(input_path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                digest.update(chunk)
        return engine, digest.hexdigest()
    except OSError:
        return ("", "")


def _result_cache_store(key: tuple[str, str], data: bytes) -> None:
    global _RESULT_CACHE_BYTES
    if not key[0] or not data or len(data) > MAX_OUTPUT_BYTES:
        return
    if key in _RESULT_CACHE:
        _RESULT_CACHE_BYTES -= len(_RESULT_CACHE.pop(key))
    while _RESULT_CACHE and _RESULT_CACHE_BYTES + len(data) > _RESULT_CACHE_MAX_BYTES:
        _, old = _RESULT_CACHE.popitem(last=False)
        _RESULT_CACHE_BYTES -= len(old)
    _RESULT_CACHE[key] = data
    _RESULT_CACHE_BYTES += len(data)


def result_embed(filename: str, label: str, size: int, desc: str, file_note: bool) -> discord.Embed:
    embed = discord.Embed(title=filename, color=0x57F287, description=desc[:4000])
    embed.add_field(name="Engine", value=label, inline=True)
    embed.add_field(name="Size", value=f"{size:,} bytes", inline=True)
    embed.set_footer(text="Output attached." if file_note else "Review before running.")
    return embed


async def process_input(ctx: commands.Context, engine: str, url: str = "", preset=None) -> None:
    spec = SUPPORTED[engine]
    label = spec["label"]
    attachments = ctx.message.attachments
    if preset is not None:
        # the .detect one-click button re-runs a source already held in memory
        filename, preset_bytes = preset
        attachment = None
        source_url = ""
    elif attachments and url.strip():
        await ctx.reply("Use either one attached file or one raw-file URL, not both.", mention_author=False)
        return
    if len(attachments) > 1:
        await ctx.reply("Please send exactly one source file per command.", mention_author=False)
        return
    if preset is None:
        attachment = attachments[0] if attachments else None
        source_url = url.strip().strip("<>")
        preset_bytes = None
    if preset is None and attachment is None and not source_url:
        await ctx.reply(
            f"Use `{spec['command']}` with one `.lua`, `.luau`, or `.txt` attachment, or a direct raw-file URL.\n"
            f"Example: `{spec['command']} https://example.com/raw/script.lua`",
            mention_author=False,
        )
        return

    if preset is not None:
        pass
    elif attachment is not None:
        filename = Path(attachment.filename).name
        if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            await ctx.reply("Unsupported file type. Only `.lua`, `.luau`, and `.txt` files are accepted.", mention_author=False)
            return
        if attachment.size > MAX_INPUT_BYTES:
            await ctx.reply(f"File is too large. Maximum size is {MAX_INPUT_BYTES:,} bytes.", mention_author=False)
            return
    else:
        try:
            source_url, filename = _validate_public_url(source_url)
        except ValueError as exc:
            await ctx.reply(f"Invalid raw-file URL: {exc}", mention_author=False)
            return

    runtime_ok, runtime_detail = runtime_status()
    if not runtime_ok:
        await ctx.reply(
            "The bot is online, but the native runtime is not ready. Missing/non-executable: "
            f"`{runtime_detail}`. Check the Render build logs.", mention_author=False,
        )
        return

    async with job_slots:
        with tempfile.TemporaryDirectory(prefix="deobf_bot_") as temp:
            workdir = Path(temp)
            input_path = workdir / filename
            output_path = workdir / f"{Path(filename).stem}_deobfuscated.luau"
            status: Optional[discord.Message] = None
            try:
                if preset_bytes is not None:
                    input_path.write_bytes(preset_bytes)
                    size = input_path.stat().st_size
                    if size == 0:
                        await ctx.reply("That file is empty.", mention_author=False)
                        return
                elif attachment is not None:
                    await attachment.save(input_path)
                    size = input_path.stat().st_size
                    if size == 0:
                        await ctx.reply("That file is empty.", mention_author=False)
                        return
                    if size > MAX_INPUT_BYTES:
                        await ctx.reply(f"File exceeds the {MAX_INPUT_BYTES:,}-byte input limit.", mention_author=False)
                        return
                else:
                    filename, size = await asyncio.to_thread(_download_url, source_url, input_path)

                status = await ctx.reply(f"Checking `{filename}`…", mention_author=False)
                detected, diagnostic = await _scan_engine(input_path)
                if detected is None:
                    print(f"scan uncertain on {filename} ({diagnostic[:120]}); proceeding with the requested engine {engine}", flush=True)
                if detected is not None and detected != engine and not (engine == "luraph_v151" and detected == "luraph_v15"):
                    detected_label = SUPPORTED[detected]["label"]
                    await status.edit(content=(
                        f"That file is **{detected_label}**. Use `{SUPPORTED[detected]['command']}` instead."
                    ))
                    return

                wait_note = ""
                if engine == "luraph_v151":
                    wait_note = " This engine can take a few minutes on bigger files."
                elif input_path.stat().st_size > 1024 * 1024:
                    wait_note = " Large file: this can take a few minutes."
                await status.edit(content=f"⚙️ Detected **{label}**. Devirtualizing `{filename}`…{wait_note}")
                start_time = time.monotonic()
                # result cache: an identical file + engine re-run is instant
                cache_key = _cache_key(engine, input_path)
                cached = _RESULT_CACHE.get(cache_key) if cache_key[0] else None
                if cached is not None:
                    output_path.write_bytes(cached)
                else:
                    go_cloud = (size >= CLOUD_V151_MIN_BYTES) if engine == "luraph_v151" else (size >= CLOUD_OTHER_MIN_BYTES)
                    if go_cloud and GH_DISPATCH_TOKEN:
                        try:
                            await status.edit(content=f"☁️ `{filename}` is a big file: running it on the free cloud runner…")
                            async with cloud_slots:
                                cloud_out = await asyncio.to_thread(
                                    _cloud_deobfuscate, engine, input_path, CLOUD_WAIT_SECONDS)
                            output_path.write_bytes(cloud_out)
                        except Exception as exc:
                            print(f"Cloud runner failed ({label}, {filename}): {type(exc).__name__}: {exc}", flush=True)
                            await status.edit(content=f"☁️ Cloud runner unavailable ({str(exc)[:120]}). Running locally instead…")
                    if not output_path.is_file():
                        start_time = time.monotonic()
                        if engine == "luraph_v151":
                            try:
                                node_bin = await asyncio.to_thread(resolve_node)
                            except Exception as exc:
                                await status.edit(content=f"⚠️ The v15.1 runtime is not ready on the server: {exc}")
                                return
                            # the v15.1 tool only accepts .lua/.luau inputs: hand it a
                            # .lua-named copy when the upload came in as .txt
                            node_input = workdir / f"{Path(filename).stem}.lua"
                            if input_path != node_input:
                                await asyncio.to_thread(shutil.copyfile, input_path, node_input)
                            command = [node_bin, str(V151_SCRIPT), str(node_input), "-o", str(output_path), "--timeout", str(max(150, JOB_TIMEOUT - 30)), "--plugin", "luraph_v15", "--max-old-space-size", "6144"]
                        else:
                            command = [PYTHON, str(DEOB_SCRIPT), str(input_path), "--obfuscator", engine,
                                       "--output", str(output_path), "--timeout", str(JOB_TIMEOUT), "--no-pypy"]
                        print(f"job start: engine={label} file={filename} bytes={input_path.stat().st_size} bot_rss={_self_rss_mb()}MB", flush=True)
                        try:
                            returncode, stdout, stderr = await _run_process(command, JOB_TIMEOUT + 15)
                        except asyncio.TimeoutError:
                            await status.edit(content=f"⏱️ Timed out processing `{filename}` after {JOB_TIMEOUT} seconds.")
                            return
                        except JobMemoryExceeded as exc:
                            print(f"Job stopped at the memory ceiling ({label}, {filename}): {exc}", flush=True)
                            await status.edit(content=(
                                f"🧠 `{filename}` needed more memory than the free server has ({exc}). "
                                "The job was stopped early so the bot stays online.\n"
                                "Try a smaller file, or run this engine on a bigger Render plan."
                            ))
                            return

                        if returncode != 0 or not output_path.is_file() or output_path.stat().st_size == 0:
                            detail = (stderr or stdout).decode("utf-8", errors="replace").strip()
                            try:
                                await status.edit(content=None, view=error_view(
                                    f"Deobfuscation failed on `{filename}`",
                                    (detail[-400:] or "No diagnostic output.") + "\n\nThe script structure may not be supported.",
                                ))
                            except discord.HTTPException:
                                await status.edit(content=(
                                    f"❌ Deobfuscation failed on `{filename}`. The script structure may not be supported.\n```text\n{detail[-400:] or 'No diagnostic output.'}\n```"
                                )[:1900])
                            print(f"Deobfuscation failed ({label}, {filename}): {detail[-2000:]}", flush=True)
                            return

                raw_output = output_path.read_text(encoding="utf-8", errors="replace")
                out_text = _prepare_deobfuscated_output(raw_output)
                output_path.write_text(out_text, encoding="utf-8", newline="\n")
                output_size = output_path.stat().st_size
                if output_size > MAX_OUTPUT_BYTES:
                    await status.edit(content=f"📦 Output too large: {output_size:,} bytes (limit {MAX_OUTPUT_BYTES:,}).")
                    return
                _result_cache_store(cache_key, output_path.read_bytes())
                elapsed_seconds = max(1, int(time.monotonic() - start_time))
                elapsed = f"{elapsed_seconds}s" if elapsed_seconds < 120 else f"{elapsed_seconds // 60}m {elapsed_seconds % 60}s"
                await status.edit(content=f"✅ Deobfuscated `{filename}` with **{label}**.")
                pastefy_url = ""
                try:
                    pastefy_url = await asyncio.to_thread(
                        _pastefy_upload, out_text.rstrip(), Path(filename).stem)
                except Exception as exc:
                    print(f"Pastefy upload error: {type(exc).__name__}: {exc}", flush=True)
                if output_size <= 1600 and "```" not in out_text:
                    await ctx.reply(view=result_view(filename, label, output_size, out_text.rstrip(), None, elapsed, pastefy_url=pastefy_url), mention_author=False)
                else:
                    await ctx.reply(
                        view=result_view(filename, label, output_size, None, output_path.name, elapsed, pastefy_url=pastefy_url),
                        file=discord.File(str(output_path), filename=output_path.name),
                        mention_author=False,
                    )
            except ValueError as exc:
                message = str(exc)
                if status:
                    await status.edit(content=message[:1900])
                else:
                    await ctx.reply(message[:1900], mention_author=False)
            except discord.Forbidden:
                print("Discord permission error: cannot read/send messages or attachments.", flush=True)
            except discord.HTTPException as exc:
                if status:
                    try:
                        await status.edit(content=f"Discord file/message error: {exc}"[:1900])
                    except discord.HTTPException:
                        pass
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                print(f"Unexpected job error: {type(exc).__name__}: {exc}", flush=True)
                message = f"Unexpected processing error: `{type(exc).__name__}`. Check Render logs."
                if status:
                    try:
                        await status.edit(content=message)
                    except discord.HTTPException:
                        pass
                else:
                    await ctx.reply(message, mention_author=False)


@bot.command(name="lrph15")
async def lrph15(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "luraph_v15", url)


@bot.command(name="lrph15.1")
async def lrph15_1(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "luraph_v151", url)

@bot.command(name="get")
async def get_cmd(ctx: commands.Context, *, url: str = "") -> None:
    """Fetch the raw content of a link and send it back."""
    url = (url or "").strip().strip("<>")
    if not url:
        await ctx.reply("Usage: `.get <url>` \u2014 fetches a link's raw content.", mention_author=False)
        return
    gh = re.match(r"https://github\.com/([^/]+)/([^/]+)/blob/(\S+)", url)
    if gh:
        url = f"https://raw.githubusercontent.com/{gh.group(1)}/{gh.group(2)}/{gh.group(3)}"
    pb = re.match(r"https?://pastebin\.com/(?:raw/)?([A-Za-z0-9]+)/?$", url)
    if pb:
        url = f"https://pastebin.com/raw/{pb.group(1)}"
    status = await ctx.reply("Fetching\u2026", mention_author=False)
    tmp = Path(tempfile.gettempdir()) / f"get_{time.time_ns() % 10**10}.bin"
    try:
        filename, size = await asyncio.to_thread(_download_url, url, tmp, True)
        base = Path(filename).name or "raw.txt"
        if not base.lower().endswith((".txt", ".lua", ".luau", ".json", ".js", ".py", ".md", ".csv", ".xml", ".html", ".ini", ".cfg", ".yml", ".yaml", ".log")):
            base = base + ".txt"
        data = tmp.read_bytes()
        text = data.decode("utf-8", errors="replace")
        pastefy_url = ""
        if size > 1800:
            try:
                pastefy_url = await asyncio.to_thread(_pastefy_upload, text, Path(filename).stem or "raw")
            except Exception as exc:
                print(f"Pastefy upload error: {type(exc).__name__}: {exc}", flush=True)
        link = f"\n\U0001f517 [Pastefy]({pastefy_url}) \u00b7 [raw]({pastefy_url}/raw)" if pastefy_url else ""
        if size <= 1800:
            await status.edit(content=f"`{filename}` ({_human_size(size)}):\n```\n{text[:1800]}\n```")
        elif size <= 7 * 1024 * 1024:
            await status.edit(content=f"`{filename}` ({_human_size(size)}) \u2014 attached below.{link}")
            await ctx.send(file=discord.File(fp=str(tmp), filename=base))
        else:
            await status.edit(content=f"`{filename}` is {_human_size(size)} \u2014 too big to attach, uploaded to Pastefy instead.{link}")
    except Exception as exc:
        await status.edit(content=f"Couldn't fetch that link: {str(exc)[:200]}")
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


@bot.command(name="iron")
async def iron(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "ironbrew1", url)


@bot.command(name="moon")
async def moon(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "moonsec_v3", url)


@bot.command(name="cent")
async def cent(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "centurion", url)


@bot.command(name="detect")
async def detect(ctx: commands.Context, *, url: str = "") -> None:
    attachments = ctx.message.attachments
    if attachments and url.strip():
        await ctx.reply("Use either one attached file or one raw-file URL, not both.", mention_author=False)
        return
    if len(attachments) > 1:
        await ctx.reply("Please send exactly one source file per command.", mention_author=False)
        return
    attachment = attachments[0] if attachments else None
    source_url = url.strip().strip("<>")
    if attachment is None and not source_url:
        await ctx.reply(
            "Use `.detect` with one `.lua`, `.luau`, or `.txt` attachment, or a direct raw-file URL.\n"
            "Example: `.detect https://example.com/raw/script.lua`",
            mention_author=False,
        )
        return
    if attachment is not None:
        filename = Path(attachment.filename).name
        if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            await ctx.reply("Unsupported file type. Only `.lua`, `.luau`, and `.txt` files are accepted.", mention_author=False)
            return
        if attachment.size > MAX_INPUT_BYTES:
            await ctx.reply(f"File is too large. Maximum size is {MAX_INPUT_BYTES:,} bytes.", mention_author=False)
            return
    else:
        try:
            source_url, filename = _validate_public_url(source_url)
        except ValueError as exc:
            await ctx.reply(f"Invalid raw-file URL: {exc}", mention_author=False)
            return
    with tempfile.TemporaryDirectory(prefix="detect_bot_") as temp:
        input_path = Path(temp) / filename
        try:
            if attachment is not None:
                await attachment.save(input_path)
                if input_path.stat().st_size == 0:
                    await ctx.reply("That file is empty.", mention_author=False)
                    return
            else:
                filename, _size = await asyncio.to_thread(_download_url, source_url, input_path)
            status = await ctx.reply(f"Analyzing `{filename}`\u2026", mention_author=False)
            start_time = time.monotonic()
            try:
                rows, basis = await _detect_scores(input_path)
            except ValueError as exc:
                await status.edit(content=str(exc)[:1900])
                return
            elapsed_seconds = max(1, int(time.monotonic() - start_time))
            elapsed = f"{elapsed_seconds}s" if elapsed_seconds < 120 else f"{elapsed_seconds // 60}m {elapsed_seconds % 60}s"
            source = None
            best = max(((c, n) for n, c, _l, _e in rows
                        if n not in ("obfuscated", "plain", "generic")), default=(0.0, ""))
            if best[0] >= 0.999 and best[1] in SUPPORTED:
                if attachment is not None:
                    source = ("attachment", filename, input_path.read_bytes())
                else:
                    source = ("url", source_url)
            try:
                await status.edit(content=None, view=detect_view(filename, rows, basis, elapsed, source=source))
            except discord.HTTPException:
                best_label = rows[0][2] if rows else "nothing"
                best_pct = int(round(rows[0][1] * 100)) if rows else 0
                await status.edit(content=f"\U0001f50d Detection: {best_label} ({best_pct}%). Your Discord client may not show the full report.")
        except discord.HTTPException:
            print("Discord permission error during .detect: cannot read/send messages.", flush=True)


@bot.command(name="deobfs", aliases=["deobfuscators", "engines"])
async def deobfs(ctx: commands.Context) -> None:
    await ctx.reply(view=info_view("Supported deobfuscators", engines_body()), mention_author=False)


@bot.command(name="help")
async def help_command(ctx: commands.Context) -> None:
    body = (
        "**SUPPORTED ENGINES**\n"
        "• **Luraph v15.1**  ·  `.lrph15.1`\n"
        "• **Luraph v15**  ·  `.lrph15`\n"
        "• **IronBrew 1**  ·  `.iron`\n"
        "• **MoonSec V3**  ·  `.moon`\n"
        "• **Centurion**  ·  `.cent`\n\n"
        "**INPUT**\n"
        "Attach one `.lua`, `.luau`, or `.txt` file, or pass a direct raw-file URL.\n\n"
        "**EXAMPLES**\n"
        "• `.detect` with a file attached\n"
        "• `.lrph15.1 https://example.com/raw/script.lua`\n"
        "• `.moon` with a MoonSec file attached\n\n"
        "**OTHER COMMANDS**\n"
        "• `.engines` — list supported engines\n"
        "• `.get <url>` — fetch raw text"
    )
    await ctx.reply(view=info_view("MonLua · Quick Guide", body), mention_author=False)


@bot.event
async def on_ready() -> None:
    ok, detail = runtime_status()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)
    if ok:
        print(f"Native runtimes found: {detail}", flush=True)
    else:
        print(f"WARNING: native runtimes missing or not executable: {detail}", flush=True)
    if not (V151_SCRIPT.is_file() and V151_NODE_ARCHIVE.is_file()):
        print("WARNING: v15.1 runtime incomplete; .lrph15.1 will be unavailable.", flush=True)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply("Please wait a moment before trying again.", mention_author=False)
        return
    print(f"Command error: {type(error).__name__}: {error}", flush=True)
    try:
        await ctx.reply("Something went wrong while handling that command. Check the Render logs.", mention_author=False)
    except discord.HTTPException:
        pass


async def main() -> None:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: DISCORD_BOT_TOKEN")
    if not DEOB_SCRIPT.is_file():
        print(
            f"WARNING: deobfuscator CLI not found: {DEOB_SCRIPT}. "
            "The bot is coming online, but deobfuscation commands will be unavailable "
            "until the deobf folder is added.",
            flush=True,
        )
    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"Bot startup failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        raise
