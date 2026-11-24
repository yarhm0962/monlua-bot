from __future__ import annotations

import asyncio
import base64
import hashlib
import html
import io
import ipaddress
import json
import os
import platform
import re
import shutil
import signal
import time
import socket
import subprocess
import sys
import traceback
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

ROOT = Path(__file__).resolve().parent
DEOB_DIR = ROOT / "deobf"
DEOB_SCRIPT = DEOB_DIR / "deob.py"
PYTHON = os.getenv("PYTHON", sys.executable or "python3")
MAX_INPUT_BYTES = max(1, int(os.getenv("MAX_INPUT_BYTES", str(32 * 1024 * 1024))))
# Sources above this can only run on the cloud runner: the local engine and the
# Env Logger execute inside this container, which has 512 MB of memory.
LOCAL_INPUT_BYTES = max(1, int(os.getenv("LOCAL_INPUT_BYTES", str(8 * 1024 * 1024))))
MAX_OUTPUT_BYTES = max(1, int(os.getenv("MAX_OUTPUT_BYTES", str(24 * 1024 * 1024))))
JOB_TIMEOUT = max(10, min(1800, int(os.getenv("DEOB_TIMEOUT", "900"))))  # 15 min headroom for ~2 MB files
MAX_CONCURRENT_JOBS = max(1, int(os.getenv("MAX_CONCURRENT_JOBS", "2")))
URL_TIMEOUT = max(5, min(180, int(os.getenv("URL_TIMEOUT", "60"))))
ALLOWED_EXTENSIONS = {".lua", ".luau", ".txt"}

ENVLOGGER_DIR = DEOB_DIR / "envlogger"
ENVLOGGER_SCRIPT = ENVLOGGER_DIR / "env_logger.luau"
ENVLOGGER_APIDUMP = ENVLOGGER_DIR / "core" / "io" / "apidump.json"
LUNE_BIN = ENVLOGGER_DIR / "bin" / "lune"
ENVLOGGER_TIMEOUT = max(30, min(600, int(os.getenv("ENVLOGGER_TIMEOUT", "120"))))
SUPPORTED = {
    "luraph_v143": {"label": "Luraph v14.3"},
    "luraph_v147": {"label": "Luraph v14.7"},
    "luraph_v148": {"label": "Luraph v14.8"},
    "luraph_v149": {"label": "Luraph v14.9"},
    "luraph_v15": {"label": "Luraph v15"},
    "luraph_v151": {"label": "Luraph v15.1"},
    "moonsec_v3": {"label": "MoonSec V3"},
    "centurion": {"label": "Centurion"},
    "moonveil_v145": {"label": "MoonVeil v1.4.5"},
    "ironbrew1": {"label": "IronBrew1"},
    "ironbrew2": {"label": "IronBrew2"},
    "ironveil_v1": {"label": "Ironveil v1"},
    "77fuscator": {"label": "77fuscator"},
    "fulcrum": {"label": "Fulcrum Deobfuscator"},
    "jayfuscator": {"label": "Jayfuscator"},
}


CHANNEL_CONFIG_PATH = Path(os.getenv("CHANNEL_CONFIG_PATH", str(ROOT / "channel_restrictions.json"))).expanduser()
CHANNEL_CONFIG_LOAD_FAILED = False


def _validate_channel_config(raw) -> dict[str, list[int]]:
    """Shape-check a raw allowlist mapping; raises ValueError on anything invalid."""
    if not isinstance(raw, dict):
        raise ValueError("expected a JSON object keyed by guild ID")
    result: dict[str, list[int]] = {}
    for guild_id, values in raw.items():
        if not str(guild_id).isdigit() or not isinstance(values, list):
            raise ValueError("invalid guild ID or channel list in settings")
        if any(not str(value).isdigit() for value in values):
            raise ValueError("invalid channel ID in settings")
        valid = sorted({int(value) for value in values})
        if valid:
            result[str(int(guild_id))] = valid
    return result


def _load_channel_restrictions() -> dict[str, list[int]]:
    """Load per-guild allowlists; malformed/unreadable settings fail closed."""
    global CHANNEL_CONFIG_LOAD_FAILED
    try:
        raw = json.loads(CHANNEL_CONFIG_PATH.read_text(encoding="utf-8"))
        return _validate_channel_config(raw)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        CHANNEL_CONFIG_LOAD_FAILED = True
        print(
            f"WARNING: channel restrictions failed to load; commands will fail closed until repaired: "
            f"{type(exc).__name__}: {exc}",
            flush=True,
        )
        return {}


def _persist_channel_restrictions(updated: dict[str, list[int]]) -> None:
    """Atomically persist settings before publishing them to the running bot."""
    temporary = CHANNEL_CONFIG_PATH.with_suffix(".json.tmp")
    try:
        temporary.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(CHANNEL_CONFIG_PATH)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass

# The service filesystem is wiped by every deploy and restart, which silently
# erased a configured /set channel allowlist. The settings are therefore
# mirrored into the private jobs repo and re-applied on boot, so a configured
# channel list survives deploys, restarts, and free-tier cold starts.
CHANNEL_CONFIG_REMOTE_PATH = "config/channel_restrictions.json"
_channel_config_remote_sha: Optional[str] = None
_channel_config_remote_lock = asyncio.Lock()
_channel_config_restored = False
_channel_backup_tasks: set[asyncio.Task] = set()


def _fetch_remote_channel_state() -> tuple[Optional[dict], Optional[str]]:
    """(validated allowlist or None, blob sha or None) from the jobs repo; both None when absent."""
    if not cloud_runner_configured():
        return None, None
    code, resp = _gh_api("GET", f"/repos/{GH_JOBS_REPO}/contents/{CHANNEL_CONFIG_REMOTE_PATH}?ref=main")
    if code == 404:
        return None, None
    if code != 200:
        print(f"WARNING: remote channel-config fetch failed: HTTP {code}", flush=True)
        return None, None
    try:
        payload = json.loads(resp)
        content = base64.b64decode(payload.get("content", "")).decode("utf-8")
        return _validate_channel_config(json.loads(content)), payload.get("sha")
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f"WARNING: remote channel-config unreadable: {type(exc).__name__}: {exc}", flush=True)
        return None, None


async def _push_channel_restrictions_remote(updated: dict[str, list[int]]) -> bool:
    """Best-effort backup of the allowlist into the jobs repo; False when it could not be stored."""
    global _channel_config_remote_sha
    if not cloud_runner_configured():
        return False
    code, resp = 0, b""
    async with _channel_config_remote_lock:
        for attempt in range(2):
            if _channel_config_remote_sha is None:
                _remote_state, _channel_config_remote_sha = await asyncio.to_thread(_fetch_remote_channel_state)
            payload = json.dumps(updated, indent=2, sort_keys=True) + "\n"
            body = {
                "message": "update MonLua command-channel settings",
                "content": base64.b64encode(payload.encode("utf-8")).decode("ascii"),
            }
            if _channel_config_remote_sha:
                body["sha"] = _channel_config_remote_sha
            code, resp = await asyncio.to_thread(
                _gh_api, "PUT", f"/repos/{GH_JOBS_REPO}/contents/{CHANNEL_CONFIG_REMOTE_PATH}", body=body
            )
            if code in (200, 201):
                try:
                    _channel_config_remote_sha = json.loads(resp)["content"]["sha"]
                except (ValueError, TypeError, KeyError):
                    pass
                return True
            if code in (409, 422) and attempt == 0:
                # stale blob sha: refetch and retry once
                _channel_config_remote_sha = None
                continue
            break
    print(f"WARNING: channel-restriction backup failed: HTTP {code}: {resp[:200]!r}", flush=True)
    return False


async def _backup_channel_restrictions_task() -> None:
    try:
        await _push_channel_restrictions_remote(
            {key: list(value) for key, value in CHANNEL_RESTRICTIONS.items()}
        )
    except Exception as exc:
        print(f"WARNING: channel-restriction backup task failed: {type(exc).__name__}: {exc}", flush=True)


def _schedule_channel_backup() -> None:
    task = asyncio.create_task(_backup_channel_restrictions_task())
    _channel_backup_tasks.add(task)
    task.add_done_callback(_channel_backup_tasks.discard)


async def _restore_channel_restrictions_remote() -> None:
    """Re-apply the persisted allowlist after a fresh container so /set channel settings survive."""
    global _channel_config_restored, _channel_config_remote_sha
    if _channel_config_restored or not cloud_runner_configured():
        return
    _channel_config_restored = True
    async with _channel_config_remote_lock:
        remote, sha = await asyncio.to_thread(_fetch_remote_channel_state)
        _channel_config_remote_sha = sha
    if remote is None:
        if CHANNEL_RESTRICTIONS:
            await _backup_channel_restrictions_task()
        return
    if {key: list(value) for key, value in CHANNEL_RESTRICTIONS.items()} != remote:
        CHANNEL_RESTRICTIONS.clear()
        CHANNEL_RESTRICTIONS.update(remote)
        try:
            _persist_channel_restrictions(remote)
        except OSError as exc:
            print(f"Couldn't cache restored channel restrictions locally: {type(exc).__name__}: {exc}", flush=True)
        print(f"Restored command-channel settings for {len(remote)} server(s) from the persisted config.", flush=True)


CHANNEL_RESTRICTIONS: dict[str, list[int]] = _load_channel_restrictions()
_channel_settings_lock = asyncio.Lock()


def _allowed_channel_ids(guild_id: Optional[int]) -> list[int]:
    if guild_id is None:
        # A DM has no guild context, so don't let it become an alternate route
        # around a server's configured command-channel policy.
        return []
    return CHANNEL_RESTRICTIONS.get(str(guild_id), [])


def _channel_is_allowed(guild_id: Optional[int], channel_id: Optional[int]) -> bool:
    if CHANNEL_CONFIG_LOAD_FAILED:
        return False
    configured = _allowed_channel_ids(guild_id)
    if guild_id is None:
        return not CHANNEL_RESTRICTIONS
    return not configured or (channel_id is not None and int(channel_id) in configured)


class ChannelRestrictionCheckFailure(commands.CheckFailure):
    """The command was blocked by this guild's configured channel policy."""


async def _prefix_channel_check(ctx: commands.Context) -> bool:
    guild_id = ctx.guild.id if ctx.guild else None
    channel_id = ctx.channel.id if ctx.channel else None
    if _channel_is_allowed(guild_id, channel_id):
        return True
    print(
        f"Blocked prefix command {ctx.command.qualified_name if ctx.command else '?'} "
        f"outside configured channel(s); guild={guild_id} channel={channel_id}",
        flush=True,
    )
    raise ChannelRestrictionCheckFailure()


class ChannelRestrictedCommandTree(app_commands.CommandTree):
    """Apply the same channel policy to every Discord slash command."""

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        qualified_name = interaction.command.qualified_name if interaction.command else ""
        # Keep the administration controls available from any channel so the
        # server can always recover from a restrictive or mistaken setting.
        if qualified_name in {"set channel", "remove set channel"}:
            return True
        guild_id = interaction.guild_id
        channel_id = interaction.channel_id
        if _channel_is_allowed(guild_id, channel_id):
            return True
        configured = _allowed_channel_ids(guild_id)
        if CHANNEL_CONFIG_LOAD_FAILED:
            message = "Command-channel settings could not be loaded. An administrator must use /set channel to repair them."
        elif guild_id is None and CHANNEL_RESTRICTIONS:
            message = "Bot commands are disabled in DMs while channel restrictions are configured."
        elif configured:
            mentions = ", ".join(f"<#{cid}>" for cid in configured)
            message = f"Commands are restricted to: {mentions}."
        else:
            message = "This command can't be used in this context."
        try:
            response_view = info_view("Command unavailable here", message)
            if interaction.response.is_done():
                await interaction.followup.send(view=response_view, ephemeral=True)
            else:
                await interaction.response.send_message(view=response_view, ephemeral=True)
        except discord.HTTPException:
            pass
        return False


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command=None,
    tree_cls=ChannelRestrictedCommandTree,
)
bot.add_check(_prefix_channel_check)
job_slots = asyncio.Semaphore(MAX_CONCURRENT_JOBS)

# Render's free instance has 512 MiB total for everything. A deobfuscation job
# that runs past this budget is stopped (with a clear error card) instead of
# letting the container OOM-kill the whole service and leave the user's
# "Devirtualizing..." message hanging forever. The budget is shared across the
# concurrent jobs MAX_CONCURRENT_JOBS allows.
JOB_MEM_BUDGET_MB = 330
_active_jobs = 0
_REQUEST_ACCEPTED_DELETE_TASKS: set[asyncio.Task] = set()


async def _delete_request_accepted_message(interaction: discord.Interaction) -> None:
    await asyncio.sleep(3)
    try:
        await interaction.delete_original_response()
    except discord.NotFound:
        pass
    except discord.HTTPException as exc:
        print(f"Request Accepted message cleanup failed: {type(exc).__name__}: {exc}", flush=True)


def _schedule_request_accepted_delete(interaction: discord.Interaction) -> None:
    task = asyncio.create_task(_delete_request_accepted_message(interaction))
    _REQUEST_ACCEPTED_DELETE_TASKS.add(task)
    task.add_done_callback(_REQUEST_ACCEPTED_DELETE_TASKS.discard)

# Free cloud runner: big jobs are dispatched to the private GitHub Actions
# repo in GH_JOBS_REPO (a runner has ~8 GB RAM and 2 dedicated cores), so big
# files finish in a couple of minutes instead of exhausting the 512 MB
# Render instance. Small files keep running locally; any cloud failure falls
# back to the local engine. Identical re-runs are answered instantly from
# _RESULT_CACHE.
GH_JOBS_REPO = os.getenv("GH_JOBS_REPO", "yarhm0962/monlua-jobs")
GH_DISPATCH_TOKEN = os.getenv("GH_DISPATCH_TOKEN", "").strip()
GH_TOKEN_PLACEHOLDERS = ("placeholder", "replace_me", "your_token", "your-token", "paste_token", "changeme")


def cloud_runner_configured() -> bool:
    token = GH_DISPATCH_TOKEN.lower()
    return len(token) >= 20 and not any(marker in token for marker in GH_TOKEN_PLACEHOLDERS)


class _LoggedLayoutView(discord.ui.LayoutView):
    """Surface component errors in the logs instead of swallowing them."""

    async def on_error(self, interaction: discord.Interaction, error: Exception, item) -> None:
        print(f"View error for {item} in {type(self).__name__}: {error!r}\n{traceback.format_exc()}", flush=True)


def info_view(title: str, body: str, color: int = 0x9C7CFF, footer: str = "") -> discord.ui.LayoutView:
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=color)
    container.add_item(discord.ui.TextDisplay(f"## {title}"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(_fit_text(body.strip())))
    if footer:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(_fit_text(f"-# {footer}")))
    view.add_item(container)
    return view


def _fit_text(value, width: int = 64) -> str:
    """Hard-wrap long lines so cards stay readable on narrow screens."""
    out = []
    for raw in str(value or "").splitlines():
        raw = raw.rstrip()
        while len(raw) > width:
            cut = raw.rfind(" ", 0, width + 1)
            if cut <= 0:
                cut = width
            out.append(raw[:cut].rstrip())
            raw = raw[cut:].lstrip()
        out.append(raw)
    return "\n".join(out)


def engines_body() -> str:
    lines = [
        "**DETECTION COVERAGE**",
        "• Luraph v14.3, v14.7, v14.8, v14.9, v15, v15.1",
        "• MoonSec V3",
        "• Centurion",
        "• MoonVeil v1.4.5 (v2.1.1 recognized)",
        "• IronBrew1, IronBrew2",
        "• Ironveil v1",
        "• 77fuscator",
        "• Fulcrum Deobfuscator",
        "• Jayfuscator",
        "",
        "**ENV LOGGER**",
        "• .l with a Lua file, raw URL, or pasted code. Runs the script in a sandbox and records decoded strings, loadstring payloads, _G writes, remotes and links.",
        "",
        "**COMMANDS**",
        "• .detect or .d. Identifies the obfuscator.",
        "• .beautify or .b. Formats source.",
        "• .get. Fetches raw source and resolves embedded loaders.",
    ]
    return "\n".join(lines)


def _is_size_limit_error(exc: BaseException) -> bool:
    """True for input-size rejections, so generic handlers show a clear card."""
    text = str(exc).lower()
    return any(
        marker in text
        for marker in (
            "input limit",
            "upload limit",
            "input too large",
            "maximum input size",
            "too large for local",
            "too large for the local",
            "capped at",
        )
    )


def _human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


LONG_COMMENT_OPEN_RE = re.compile(r"--\[(=*)\[")
LONG_STRING_OPEN_RE = re.compile(r"\[(=*)\[")


def _strip_lua_comments(source: str) -> str:
    out = []
    i, n = 0, len(source)
    line_start = 0
    newline = chr(10)
    while i < n:
        if source.startswith("--", i):
            line_end = source.find(newline, i)
            if line_end < 0:
                line_end = n
            stripped = source[i:line_end].strip()
            if source[line_start:i].strip() == "" and (
                (stripped.startswith("-- [[ Deobfuscated by") and stripped.endswith("]]"))
                or (stripped.startswith("-- Deobfuscated by MonLua") and stripped.endswith("]"))
            ):
                i = line_end + (1 if line_end < n else 0)
                line_start = i
                continue
            long_comment = LONG_COMMENT_OPEN_RE.match(source, i)
            if long_comment:
                close = "]" + long_comment.group(1) + "]"
                end = source.find(close, long_comment.end())
                end = n if end < 0 else end + len(close)
                removed_lines = source[i:end].count(newline)
                out.append(newline * removed_lines if removed_lines else " ")
                last_newline = source.rfind(newline, i, end)
                if last_newline >= 0:
                    line_start = last_newline + 1
                i = end
            else:
                out.append(newline if line_end < n else "")
                i = line_end + (1 if line_end < n else 0)
                line_start = i
            continue
        if source[i] in ('"', "'", chr(96)):
            quote = source[i]
            start = i
            i += 1
            while i < n:
                if source[i] == chr(92):
                    i += 2
                    continue
                if source[i] == newline:
                    line_start = i + 1
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            out.append(source[start:i])
            continue
        if source[i] == "[":
            long_string = LONG_STRING_OPEN_RE.match(source, i)
            if long_string:
                close = "]" + long_string.group(1) + "]"
                start = i
                end = source.find(close, long_string.end())
                i = n if end < 0 else end + len(close)
                last_newline = source.rfind(newline, start, i)
                if last_newline >= 0:
                    line_start = last_newline + 1
                out.append(source[start:i])
                continue
        if source[i] == newline:
            line_start = i + 1
        out.append(source[i])
        i += 1
    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", "".join(out)).strip()

def _beautify_lua(source: str) -> str:
    """Use StyLua when installed; otherwise use the bundled Luau token formatter."""
    body = source.strip()
    if not body:
        return ""
    if len(body) > MAX_FORMAT_BYTES:
        return body
    stylua = _resolve_stylua() or shutil.which("stylua")
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


def _finish_output(source: str, header: str) -> str:
    """Keep one provenance header, remove all other comments, and beautify the code."""
    body = _strip_lua_comments(source.lstrip("\ufeff"))
    formatted = _beautify_lua(body)
    return f"{header}\n\n{formatted.rstrip()}\n"




PASTEFY_API_URL = "https://pastefy.app/api/v2/paste"
PASTEFY_TOKEN = (os.getenv("PASTEFY_TOKEN") or os.getenv("PASTEFY_API_TOKEN") or "").strip()
PASTEFY_TIMEOUT = max(5, min(45, int(os.getenv("PASTEFY_TIMEOUT", "20"))))
PASTEFY_CHUNK_CHARS = 450_000
RUBIS_API_URL = "https://api.rubis.app/v2/scrap"
PUBLIC_SERVICE_URL = os.getenv("PUBLIC_SERVICE_URL", "https://monlua-bot-zswa.onrender.com").rstrip("/")
RUBIS_TIMEOUT = max(5, min(60, int(os.getenv("RUBIS_TIMEOUT", "30"))))
RUBIS_CHUNK_CHARS = 2_900_000  # the free Epique plan caps scraps at 3 MB
MAX_FORMAT_BYTES = max(128_000, int(os.getenv("MAX_FORMAT_BYTES", str(256 * 1024))))   # per paste; stays under Pastefy's ~1 MB request cap even with JSON escaping

STYLUA_VERSION = "2.6.0"
STYLUA_RELEASES = {
    ("linux", "x86_64"): (
        "https://github.com/JohnnyMorganz/StyLua/releases/download/v2.6.0/stylua-linux-x86_64-musl.zip",
        "48ee7db28346f96f4bd545e190ab080a88a7b5a664e97649cf5d5c60426f402d",
        "stylua",
    ),
    ("linux", "aarch64"): (
        "https://github.com/JohnnyMorganz/StyLua/releases/download/v2.6.0/stylua-linux-aarch64.zip",
        "8e67539e5fdf7a81cd03cf592b0df18d3bb96ee17a5ea5d9bf67b86387b903b0",
        "stylua",
    ),
    ("windows", "amd64"): (
        "https://github.com/JohnnyMorganz/StyLua/releases/download/v2.6.0/stylua-windows-x86_64.zip",
        "fd13b4014e3b779c244bbc03f2c282e357f15bc526de6a6fa5ecbc447538313c",
        "stylua.exe",
    ),
}
MAX_BEAUTIFY_INLINE_CHARS = 9000


def _resolve_stylua() -> Optional[str]:
    configured = os.getenv("STYLUA_BIN", "").strip()
    if configured and Path(configured).is_file():
        return configured
    installed = shutil.which("stylua")
    if installed:
        return installed
    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine in {"amd64", "x64"}:
        machine = "amd64" if system == "windows" else "x86_64"
    release = STYLUA_RELEASES.get((system, machine))
    if release is None:
        return None
    download_url, expected_sha256, executable_name = release
    cache_dir = Path(tempfile.gettempdir()) / f"monlua-stylua-{STYLUA_VERSION}"
    executable_path = cache_dir / executable_name
    if executable_path.is_file() and (system == "windows" or os.access(executable_path, os.X_OK)):
        return str(executable_path)
    try:
        request = urllib.request.Request(
            download_url,
            headers={"User-Agent": "MonLua-Beautifier/1.0", "Accept": "application/octet-stream"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            archive_data = response.read(8 * 1024 * 1024 + 1)
        if len(archive_data) > 8 * 1024 * 1024:
            raise ValueError("the StyLua release archive exceeded its expected size")
        if hashlib.sha256(archive_data).hexdigest() != expected_sha256:
            raise ValueError("the StyLua release archive failed its SHA-256 integrity check")
        with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
            matches = [
                item for item in archive.infolist()
                if not item.is_dir() and Path(item.filename).name == executable_name
            ]
            if len(matches) != 1:
                raise ValueError("the StyLua release archive did not contain one expected executable")
            executable_data = archive.read(matches[0])
        if not executable_data or len(executable_data) > 20 * 1024 * 1024:
            raise ValueError("the downloaded StyLua executable has an invalid size")
        cache_dir.mkdir(parents=True, exist_ok=True)
        temporary = executable_path.with_suffix(executable_path.suffix + ".tmp")
        temporary.write_bytes(executable_data)
        if system != "windows":
            temporary.chmod(0o755)
        temporary.replace(executable_path)
        return str(executable_path)
    except (OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError, TimeoutError) as exc:
        print(f"StyLua {STYLUA_VERSION} could not be installed: {type(exc).__name__}: {exc}", flush=True)
        return None


def _unwrap_lua_code_block(source: str) -> str:
    value = (source or "").strip()
    fence = chr(96) * 3
    pattern = re.escape(fence) + r"(?:lua|luau)?[ \t]*\r?\n(.*?)\r?\n" + re.escape(fence)
    match = re.fullmatch(pattern, value, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return value


def _beautify_source(source: str, filename: str) -> str:
    body = _unwrap_lua_code_block(source).lstrip("\ufeff")
    if not body.strip():
        raise ValueError("The supplied source is empty.")
    if len(body.encode("utf-8")) > MAX_FORMAT_BYTES:
        raise ValueError(f"Source exceeds the {_human_size(MAX_FORMAT_BYTES)} beautification limit.")
    stylua = _resolve_stylua()
    if not stylua:
        raise RuntimeError(
            "StyLua 2.6.0 is unavailable for this system. Install StyLua and make it available "
            "on PATH, or set STYLUA_BIN to its executable."
        )
    try:
        result = subprocess.run(
            [
                stylua,
                "--verify",
                "--no-editorconfig",
                "--column-width",
                "100",
                "--indent-type",
                "Spaces",
                "--indent-width",
                "4",
                "--line-endings",
                "Unix",
                "--stdin-filepath",
                filename if Path(filename).suffix.lower() in {".lua", ".luau"} else "input.lua",
                "-",
            ],
            input=body,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("StyLua did not finish formatting this source within 30 seconds.") from exc
    except OSError as exc:
        raise RuntimeError(f"Could not start the StyLua formatter: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "No parser details were returned.").strip()
        raise ValueError(f"Lua formatting failed because the source could not be parsed or verified: {detail[:650]}")
    formatted = result.stdout.strip()
    if not formatted:
        raise ValueError("The formatter returned an empty result.")
    if len(formatted.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise ValueError(f"Formatted output exceeds the {_human_size(MAX_OUTPUT_BYTES)} output limit.")
    return formatted + "\n"


def _split_beautified_source(source: str, max_chars: int) -> list[str]:
    if max_chars <= 0:
        return [source]
    chunks = []
    current = ""
    for line in source.splitlines(keepends=True):
        while len(line) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:max_chars])
            line = line[max_chars:]
        if current and len(current) + len(line) > max_chars:
            chunks.append(current)
            current = line
        else:
            current += line
    if current:
        chunks.append(current)
    return chunks or [source]


def _beautify_filename(filename: str) -> str:
    raw_name = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(filename).name).strip("._")
    suffix = Path(raw_name).suffix.lower()
    if suffix not in {".lua", ".luau"}:
        suffix = ".lua"
    stem = Path(raw_name).stem[:100] or "beautified"
    return stem + suffix


async def _send_beautified_output(ctx: commands.Context, filename: str, source: str) -> None:
    safe_name = _beautify_filename(filename)
    if len(source) <= MAX_BEAUTIFY_INLINE_CHARS:
        longest_ticks = max(
            (len(match) for match in re.findall(re.escape(chr(96)) + r"+", source)),
            default=2,
        )
        fence = chr(96) * max(3, longest_ticks + 1)
        capacity = min(1500, 1850 - 2 * len(fence) - 16)
        if capacity >= 100:
            chunks = _split_beautified_source(source, capacity)
            total = len(chunks)
            for index, chunk in enumerate(chunks, 1):
                heading = "**Beautified Lua** · " + safe_name
                if total > 1:
                    heading += f"\n-# Part {index} of {total}"
                content = f"{heading}\n\n{fence}lua\n{chunk}\n{fence}"
                if index == 1:
                    await ctx.reply(
                        content=content,
                        mention_author=False,
                        allowed_mentions=discord.AllowedMentions.none(),
                    )
                else:
                    await ctx.send(
                        content=content,
                        allowed_mentions=discord.AllowedMentions.none(),
                    )
            return
    encoded = source.encode("utf-8")
    content = (
        f"**Lua beautified** · {safe_name}\n"
        f"**Output size** · {_human_size(len(encoded))}\n"
        "The complete formatted source is attached."
    )
    await ctx.reply(
        content=content,
        file=discord.File(fp=io.BytesIO(encoded), filename=safe_name),
        mention_author=False,
        allowed_mentions=discord.AllowedMentions.none(),
    )




def _pastefy_post(payload: dict):
    headers = {"Content-Type": "application/json"}
    # Pastefy's API expects the token as a Bearer header, not a raw value.
    attempts = ([{"Authorization": f"Bearer {PASTEFY_TOKEN}"}] if PASTEFY_TOKEN else []) + [{}]
    for auth in attempts:
        tagged = "with API token" if auth else "anonymous"
        try:
            request = urllib.request.Request(
                PASTEFY_API_URL, data=json.dumps(payload).encode("utf-8"),
                headers={**headers, **auth})
            with urllib.request.urlopen(request, timeout=PASTEFY_TIMEOUT) as response:
                data = json.loads(response.read().decode("utf-8", errors="replace"))
            paste = data.get("paste") or {}
            if paste.get("id"):
                if auth:
                    print("Pastefy upload OK with API token.", flush=True)
                return paste
            print(f"Pastefy upload rejected ({tagged}): {str(data)[:200]}", flush=True)
            if auth and PASTEFY_TOKEN:
                print("Pastefy rejected the API token; uploads fall back to anonymous. Check PASTEFY_TOKEN.", flush=True)
        except Exception as exc:
            print(f"Pastefy upload failed ({tagged}): {type(exc).__name__}: {exc}", flush=True)
    return None


def _pastefy_upload(text: str, title: str) -> str:
    """Upload output to Pastefy; outputs past the ~1 MB per-paste cap are split into
    numbered parts with an index paste holding every link. Returns the paste URL or ""."""
    if not text:
        return ""
    part_count = (len(text) + PASTEFY_CHUNK_CHARS - 1) // PASTEFY_CHUNK_CHARS
    urls = []
    for index in range(part_count):
        chunk = text[index * PASTEFY_CHUNK_CHARS:(index + 1) * PASTEFY_CHUNK_CHARS]
        part_title = title[:110] if part_count == 1 else f"{title[:96]} ({index + 1}/{part_count})"
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
    return ""


def _rubis_proxy_raw_url(scrap_id) -> str:
    """Raw links go through the bot's own raw viewer: browsers (Discord's in-app
    one included) download plain-text links, and this route answers browsers
    with a view-only HTML page while HttpGet callers get identical raw bytes."""
    scrap_id = str(scrap_id or "").strip()
    if scrap_id:
        return f"{PUBLIC_SERVICE_URL}/rubis/{scrap_id}"
    return ""


def _rubis_post(text: str, title: str):
    from urllib.parse import quote
    url = f"{RUBIS_API_URL}?public=true&title={quote(title[:200])}"
    try:
        request = urllib.request.Request(
            url, data=text.encode("utf-8"),
            headers={"Content-Type": "text/plain; charset=utf-8",
                     "User-Agent": "monlua-bot/2.0"}, method="POST")
        with urllib.request.urlopen(request, timeout=RUBIS_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
        if data.get("success") and data.get("scrapID"):
            return data
        print(f"Rubis upload rejected: {str(data)[:200]}", flush=True)
    except Exception as exc:
        print(f"Rubis upload failed: {type(exc).__name__}: {exc}", flush=True)
    return None


def _rubis_upload(text: str, title: str) -> tuple[str, str]:
    """Upload output to Rubis; returns (view URL, raw URL) or ("", "").
    Scraps past the 3 MB free-plan cap are split into numbered parts with an
    index scrap holding every link."""
    if not text:
        return "", ""
    part_count = (len(text) + RUBIS_CHUNK_CHARS - 1) // RUBIS_CHUNK_CHARS
    scraps = []
    for index in range(part_count):
        chunk = text[index * RUBIS_CHUNK_CHARS:(index + 1) * RUBIS_CHUNK_CHARS]
        part_title = title[:200] if part_count == 1 else f"{title[:180]} ({index + 1}/{part_count})"
        scrap = _rubis_post(chunk, part_title)
        if not scrap:
            return "", ""
        scraps.append(scrap)
    if part_count == 1:
        scrap = scraps[0]
        raw_url = _rubis_proxy_raw_url(scrap.get("scrapID")) or (scrap.get("raw") or "")
        return (scrap.get("view") or f"https://rubis.app/view/?scrap={scrap['scrapID']}",
                raw_url)
    urls = [item.get("view") or f"https://rubis.app/view/?scrap={item['scrapID']}" for item in scraps]
    index_text = "Full output split across Rubis parts (in order):\n\n" + "\n".join(
        f"Part {i}: {u}" for i, u in enumerate(urls, 1))
    index = _rubis_post(index_text, f"{title[:180]} - index")
    if not index:
        return "", ""
    raw_url = _rubis_proxy_raw_url(index.get("scrapID")) or (index.get("raw") or "")
    return (index.get("view") or f"https://rubis.app/view/?scrap={index['scrapID']}",
            raw_url)


def _upload_output(text: str, title: str) -> tuple[str, str, str]:
    """Give oversized output an online home: Rubis first, Pastefy as the fallback.
    Returns (service name, view URL, raw URL); empty strings when both fail."""
    text = text or ""
    if not text:
        return "", "", ""
    rubis_view, rubis_raw = _rubis_upload(text, title)
    if rubis_view:
        return "Rubiš", rubis_view, rubis_raw
    pastefy_url = _pastefy_upload(text, title)
    if pastefy_url:
        return "Pastefy", pastefy_url, pastefy_url.rstrip("/") + "/raw"
    return "", "", ""


def _online_action_row(online: tuple[str, str, str]) -> discord.ui.ActionRow:
    """Link buttons for an online copy of an output, the Components V2 way."""
    service_name, online_url, online_raw = online
    row = discord.ui.ActionRow(
        discord.ui.Button(style=discord.ButtonStyle.link, label=f"Open {service_name}", url=online_url))
    if online_raw:
        row.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="View raw", url=online_raw))
    return row


def result_view(filename: str, label: str, size: int, code_text, file_name, elapsed: str = "", online_copy=None, source_name: str = "") -> discord.ui.LayoutView:
    """Create a compact result card with a clear hierarchy on narrow screens."""
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=0x57F287)
    container.add_item(discord.ui.TextDisplay(f"## ✅ {label}"))
    output_name = (file_name or filename or "").strip()
    summary = f"**Output** · `{output_name[:64]}` · {_human_size(size)}"
    if source_name and source_name.strip() and source_name.strip() != output_name:
        summary += f"\n**Input** · `{source_name.strip()[:64]}`"
    if elapsed:
        summary += f"\n**Time** · {elapsed}"
    container.add_item(discord.ui.TextDisplay(summary))
    container.add_item(discord.ui.Separator())
    if code_text is not None:
        container.add_item(discord.ui.TextDisplay(f"```lua\n{_fit_text(code_text, 72)}\n```"))
    if file_name is not None:
        container.add_item(discord.ui.File(discord.UnfurledMediaItem(f"attachment://{file_name}")))
        container.add_item(discord.ui.TextDisplay("📎 **Output file attached**"))
    if online_copy and online_copy[1]:
        container.add_item(_online_action_row(online_copy))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay("-# Review the output before running it."))
    view.add_item(container)
    return view


async def _deliver_deobf_output(
    ctx,
    status,
    source_name: str,
    label: str,
    output_path: Path,
    output_size: int,
    out_text: Optional[str],
    elapsed: str,
) -> bool:
    out_name = output_path.name
    upload_limit = int(getattr(getattr(ctx, "guild", None), "filesize_limit", 8 * 1024 * 1024) or (8 * 1024 * 1024))
    modes = []
    if output_size <= 1600 and out_text is not None and chr(96) * 3 not in out_text:
        modes.append("inline")
    if output_size <= upload_limit:
        modes.append("attachment")
    modes.append("online")
    failures = []
    online = ("", "", "")

    for mode in modes:
        try:
            if mode == "inline":
                await ctx.reply(
                    view=result_view(out_name, label, output_size, out_text.rstrip(), None, elapsed, source_name=source_name),
                    mention_author=False,
                )
            elif mode == "attachment":
                await ctx.reply(
                    view=result_view(out_name, label, output_size, None, out_name, elapsed, source_name=source_name),
                    file=discord.File(str(output_path), filename=out_name),
                    mention_author=False,
                )
            else:
                if out_text is None:
                    out_text = await asyncio.to_thread(output_path.read_text, encoding="utf-8", errors="replace")
                online = await asyncio.to_thread(_upload_output, out_text.rstrip(), Path(out_name).stem)
                if not online[1]:
                    raise RuntimeError("The online output service did not return a complete output link.")
                await ctx.reply(
                    view=result_view(out_name, label, output_size, None, None, elapsed, online_copy=online, source_name=source_name),
                    mention_author=False,
                )
            break
        except Exception as exc:
            failures.append(f"{type(exc).__name__}: {str(exc)[:240]}")
    else:
        details = "\n".join(failures[-3:]) or "Discord and online delivery methods failed."
        if online[1]:
            details += f"\nOnline copy: {online[1]}"
        try:
            await status.edit(content=None, view=error_view("Output delivery failed", details[:850]))
        except discord.HTTPException:
            pass
        return False

    try:
        await status.delete()
    except discord.HTTPException:
        try:
            await status.edit(
                content=None,
                view=info_view("✅ Output delivered", f"**{label}** · {_human_size(output_size)}\nThe output was sent above.", color=0x57F287),
            )
        except discord.HTTPException:
            pass
    return True



def error_view(title: str, detail: str) -> discord.ui.LayoutView:
    view = _LoggedLayoutView()
    container = discord.ui.Container(accent_color=0xED4245)
    container.add_item(discord.ui.TextDisplay(f"## ⚠️ {title}"))
    container.add_item(discord.ui.Separator())
    safe_detail = _fit_text(str(detail or "No diagnostic details were provided.").strip()[-900:])
    safe_detail = safe_detail.replace("```", "`\u200b``")
    container.add_item(discord.ui.TextDisplay(f"```text\n{safe_detail}\n```"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay("**Try next**\n`.detect` identifies the engine · `.help` lists commands"))
    view.add_item(container)
    return view


DETECT_HEADER_HINTS = ("luraph", "moonsec", "ironbrew", "ironveil", "77fuscator", "fulcrum")


def detect_view(filename: str, rows, basis: str, elapsed: str = "") -> discord.ui.LayoutView:
    """Report card for `.detect` (Components V2): the identified engine with
    its confidence and the signals behind the score."""
    rows = [(n, c, l, e) for n, c, l, e in rows if n != "generic"]
    general = next(((c, l, e) for n, c, l, e in rows if n in ("obfuscated", "plain")), None)
    engines = [(n, c, l, e) for n, c, l, e in rows if n not in ("obfuscated", "plain")]
    best_name, best_conf, best_label, best_ev = engines[0] if engines else ("", 0.0, "", [])
    matched = best_conf >= 0.75
    partial = 0.30 <= best_conf < 0.75
    unknown_score = general[0] if general else 0.0
    if matched:
        title = "### \U0001f50d Obfuscator Identified"
    elif partial and (unknown_score < 0.5 or best_conf >= unknown_score):
        title = "### \U0001f50d Possible match"
    elif general and general[0] >= 0.5:
        title = "### \U0001f50d Obfuscated, engine not supported"
    elif general:
        title = "### \u2139\ufe0f No obfuscation detected"
    else:
        title = "### \u2753 Unknown obfuscator"
    head = f"-# Source: `{filename[:64]}`"
    if elapsed:
        head += f" \u00b7 \u23f1\ufe0f {elapsed}"
    body: list[str] = []
    if matched or partial:
        verdict = "Identified" if matched else "Likely"
        body.append(f"**{verdict}:** {best_label}")
        body.append(f"**Confidence:** {int(round(best_conf * 100))}%")
        others = [(l, c) for n, c, l, e in engines[1:] if c > 0]
        ev = best_ev
    elif general and general[0] >= 0.5:
        body.append(f"Obfuscated ({int(round(general[0] * 100))}% structural match), but no supported engine or known family fits.")
        body.append("Likely a custom or private obfuscator.")
        others = [(l, c) for n, c, l, e in engines if c > 0]
        ev = general[2]
    elif general:
        body.append("This script looks **unobfuscated** \u2014 no engine or known obfuscator family matched it.")
        others = []
        ev = []
    else:
        body.append("No engine reached the 75% confidence threshold.")
        others = [(l, c) for n, c, l, e in engines if c > 0]
        ev = []
    body.append(f"-# Matched by {basis}")
    if others:
        others_text = " \u00b7 ".join(f"{lab} ({int(round(c * 100))}%)" for lab, c in others[:3])
        body.append(f"-# Other matches: {others_text}")
    if ev:
        shown = " \u00b7 ".join(str(x) for x in ev[:3] if str(x))
        body.append(f"-# Evidence: {shown}")
    body.append("-# \U0001f4a1 .detect identifies only. Run .l with the file to trace it in the Env Logger")
    view = _LoggedLayoutView()
    container = discord.ui.Container()
    container.add_item(discord.ui.TextDisplay(f"{title}\n{head}"))
    container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.small))
    container.add_item(discord.ui.TextDisplay(_fit_text("\n".join(body))))
    view.add_item(container)
    return view


def _normalize_get_url(url: str) -> str:
    """Normalize common share-page URLs to their direct/raw endpoints when known."""
    value = (url or "").strip().strip("<>").strip()
    parsed = urllib.parse.urlparse(value)
    host = (parsed.hostname or "").lower()
    path = parsed.path

    match = re.match(r"^/([^/]+)/([^/]+)/blob/(.+)$", path)
    if host == "github.com" and match:
        owner, repository, rest = match.groups()
        return urllib.parse.urlunparse((
            "https", "raw.githubusercontent.com",
            f"{owner}/{repository}/{rest}", "", parsed.query, ""
        ))

    match = re.match(r"^/([^/]+)/([^/]+)/raw/(.+)$", path)
    if host == "github.com" and match:
        owner, repository, rest = match.groups()
        return urllib.parse.urlunparse((
            "https", "raw.githubusercontent.com",
            f"{owner}/{repository}/{rest}", "", parsed.query, ""
        ))

    if host in {"pastebin.com", "www.pastebin.com"}:
        match = re.match(r"^/(?:raw/)?([A-Za-z0-9]+)/?$", path)
        if match:
            return "https://pastebin.com/raw/" + match.group(1)

    if host in {"rentry.co", "www.rentry.co"}:
        slug = path.strip("/").split("/", 1)[0]
        if slug and slug != "raw":
            return f"https://rentry.co/{urllib.parse.quote(slug)}/raw"

    if host in {"hastebin.com", "www.hastebin.com"}:
        slug = path.strip("/").split("/")[-1]
        if slug and slug != "raw":
            return f"https://hastebin.com/raw/{urllib.parse.quote(slug)}"

    if host in {"paste.ee", "www.paste.ee"}:
        match = re.match(r"^/(?:p|r)/([A-Za-z0-9]+)/?$", path)
        if match:
            return f"https://paste.ee/r/{match.group(1)}"

    if host in {"pastefy.app", "www.pastefy.app"}:
        parts = [part for part in path.split("/") if part]
        if parts and parts[0] not in {"raw", "api"}:
            return f"https://pastefy.app/{urllib.parse.quote(parts[0])}/raw"

    return value


def _command_input_url(raw: str) -> str:
    """Accept a bare URL, a loadstring(...) wrapper line, or a loader link and
    return the URL to fetch: wrapper lines yield their embedded URL, share
    pages normalize to raw endpoints, loader links resolve to the hidden boot
    route so the real script is recovered instead of the decoy."""
    value = (raw or "").strip().strip("<>").strip()
    if not value.lower().startswith(("http://", "https://")):
        lowered = value.lower()
        if "\n" not in value and "loadstring" in lowered and ("http://" in lowered or "https://" in lowered):
            found = _extract_loadstring_urls(value)
            if found:
                value = found[0]
    value = _normalize_get_url(value)
    boot = _loader_boot_url(value)
    return boot or value


def _looks_like_url_argument(value: str) -> bool:
    """True when the argument is a URL fetch, not pasted code: a bare URL or a
    single-line loadstring(...) wrapper. Multi-line input stays pasted code."""
    stripped = (value or "").strip().strip("<>").strip()
    if "\n" in stripped or "\r" in stripped:
        return False
    if stripped.lower().startswith(("http://", "https://")):
        return True
    lowered = stripped.lower()
    if "loadstring" in lowered and ("http://" in lowered or "https://" in lowered):
        return bool(_extract_loadstring_urls(stripped))
    return False


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


_EXECUTOR_UA = "Roblox/Win64"
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


def _read_lua_string_literal(source: str, start: int) -> tuple[Optional[str], int]:
    if start >= len(source):
        return None, start
    quote = source[start]
    if quote in ("'", '"'):
        output = []
        index = start + 1
        while index < len(source):
            char = source[index]
            if char == quote:
                return "".join(output), index + 1
            if char != "\\":
                output.append(char)
                index += 1
                continue
            index += 1
            if index >= len(source):
                break
            escaped = source[index]
            if escaped == "x" and index + 2 < len(source) and re.fullmatch(r"[0-9a-fA-F]{2}", source[index + 1:index + 3]):
                output.append(chr(int(source[index + 1:index + 3], 16)))
                index += 3
                continue
            if escaped == "u" and index + 1 < len(source) and source[index + 1] == "{":
                close = source.find("}", index + 2)
                digits = source[index + 2:close] if close >= 0 else ""
                if close >= 0 and re.fullmatch(r"[0-9a-fA-F]{1,8}", digits):
                    try:
                        output.append(chr(int(digits, 16)))
                        index = close + 1
                        continue
                    except ValueError:
                        pass
            if escaped.isdigit():
                finish = index
                while finish < min(index + 3, len(source)) and source[finish].isdigit():
                    finish += 1
                output.append(chr(int(source[index:finish], 10) % 256))
                index = finish
                continue
            if escaped == "z":
                index += 1
                while index < len(source) and source[index].isspace():
                    index += 1
                continue
            output.append({"n": "\n", "r": "\r", "t": "\t"}.get(escaped, escaped))
            index += 1
        return None, index
    if quote == "[":
        match = LONG_STRING_OPEN_RE.match(source, start)
        if match:
            close = "]" + match.group(1) + "]"
            finish = source.find(close, match.end())
            if finish < 0:
                return source[match.end():], len(source)
            value = source[match.end():finish]
            if value.startswith("\r\n"):
                value = value[2:]
            elif value.startswith("\n"):
                value = value[1:]
            return value, finish + len(close)
    return None, start


def _extract_loadstring_urls(source: bytes | str) -> list[str]:
    text = source.decode("utf-8-sig", errors="replace") if isinstance(source, bytes) else source
    code = _strip_lua_comments(text)
    all_urls: list[str] = []
    index = 0
    while index < len(code):
        char = code[index]
        if char in ("'", '"') or (char == "[" and LONG_STRING_OPEN_RE.match(code, index)):
            _, index = _read_lua_string_literal(code, index)
            continue
        if char.isalpha() or char == "_":
            finish = index + 1
            while finish < len(code) and (code[finish].isalnum() or code[finish] == "_"):
                finish += 1
            if code[index:finish].lower() != "loadstring":
                index = finish
                continue
            opening = finish
            while opening < len(code) and code[opening].isspace():
                opening += 1
            if opening >= len(code) or code[opening] != "(":
                index = finish
                continue
            depth = 1
            cursor = opening + 1
            candidates = []
            while cursor < len(code) and depth:
                current = code[cursor]
                if current in ("'", '"') or (current == "[" and LONG_STRING_OPEN_RE.match(code, cursor)):
                    literal, next_cursor = _read_lua_string_literal(code, cursor)
                    if literal is not None:
                        cleaned = literal.replace(r"\/", "/").replace("&amp;", "&").strip()
                        match = re.search(r"https?://[^\s\"'<>]+", cleaned, re.IGNORECASE)
                        if match:
                            candidates.append((cursor, match.group(0).rstrip(".,);]}")))
                    cursor = max(next_cursor, cursor + 1)
                    continue
                if current == "(":
                    depth += 1
                elif current == ")":
                    depth -= 1
                cursor += 1
            if candidates:
                candidates.sort(key=lambda item: item[0])
                all_urls.extend(candidate[1] for candidate in candidates)
            index = max(cursor, finish)
            continue
        index += 1
    return all_urls


def _extract_loadstring_url(source: bytes | str) -> Optional[str]:
    urls = _extract_loadstring_urls(source) or []
    return urls[0] if urls else None


def _download_get_source(
    url: str,
    destination: Path,
    max_loader_depth: int = 4,
    request_timeout: int = 15,
    chain_budget_seconds: int = 120,
) -> tuple[str, int, int, Optional[str]]:
    """Fetch raw source, then follow every embedded loadstring link that works.

    Each request is short and the whole chain has a time budget, so one dead
    link in a loader can no longer stall the command; the first embedded URL
    that downloads wins, and further candidates are tried when one fails."""
    seen: set[str] = set()
    last_body: Optional[bytes] = None
    last_filename = "raw.lua"
    note: Optional[str] = None
    blocked_note: Optional[str] = None
    resolved_depth = 0
    chain_deadline = time.monotonic() + chain_budget_seconds

    with tempfile.TemporaryDirectory(prefix="monlua_get_") as workspace:
        stage = Path(workspace) / "download.bin"
        pending_urls: list[str] = [_normalize_get_url(url)]
        iteration = 0
        while pending_urls and time.monotonic() < chain_deadline:
            followed = False
            for candidate in pending_urls:
                current_url = _normalize_get_url(candidate)
                try:
                    validated_url, _filename = _validate_public_url(current_url, allow_any_ext=True)
                except ValueError as exc:
                    blocked_note = f"An embedded URL was blocked by URL safety checks: {exc}"
                    continue
                if validated_url in seen:
                    continue
                seen.add(validated_url)
                try:
                    filename, _size = _download_url(
                        validated_url, stage, allow_any_ext=True,
                        timeout=request_timeout, max_attempts=2,
                    )
                    body = stage.read_bytes()
                except (ValueError, OSError) as exc:
                    if last_body is None:
                        raise
                    note = f"Couldn't follow an embedded loadstring URL ({str(exc)[:150]})."
                    continue
                last_body = body
                last_filename = filename
                followed = True
                break
            if not followed:
                break
            if iteration > 0:
                resolved_depth += 1
            iteration += 1
            nested_urls = _extract_loadstring_urls(last_body)
            if not nested_urls:
                destination.write_bytes(last_body)
                return last_filename, len(last_body), resolved_depth, note
            if resolved_depth >= max_loader_depth:
                note = f"Loader nesting limit reached ({max_loader_depth}); returned the last fetched loader."
                break
            pending_urls = nested_urls

        if last_body is None:
            raise ValueError(blocked_note or note or "No source content could be fetched.")
        if note is None:
            if blocked_note:
                note = blocked_note
            elif pending_urls and time.monotonic() >= chain_deadline:
                note = f"Stopped following the loadstring chain after {chain_budget_seconds}s; returned the deepest source reached."
            elif pending_urls:
                note = "A repeating loadstring URL was detected; returned the last non-repeating source."
        destination.write_bytes(last_body)
        return last_filename, len(last_body), resolved_depth, note


def _download_url(url: str, destination: Path, allow_any_ext: bool = False, timeout: int = URL_TIMEOUT, max_attempts: int = 2) -> tuple[str, int]:
    current_url = url
    last_net_error: Optional[Exception] = None
    opener = urllib.request.build_opener(_NoRedirect)
    for attempt in range(max_attempts):  # one retry for transient network drops
        if attempt:
            time.sleep(2)             # brief backoff, then the same ladder again
        for _ in range(4):
            current_url, filename = _validate_public_url(current_url, allow_any_ext=allow_any_ext)
            response = None
            refused: Optional[urllib.error.HTTPError] = None
            for agent, accept in ((_EXECUTOR_UA, "*/*"), (_BROWSER_UA, "text/html,application/xhtml+xml,text/plain,application/octet-stream,*/*"), (_BOT_UA, "text/html,application/xhtml+xml,text/plain,application/octet-stream,*/*")):
                request = urllib.request.Request(current_url, headers={
                    "User-Agent": agent,
                    "Accept": accept,
                    "Accept-Language": "en-US,en;q=0.9",
                })
                try:
                    response = opener.open(request, timeout=timeout)
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
                    _validate_public_url(final_url, allow_any_ext=allow_any_ext)
                content_type = response.headers.get_content_type().lower()
                declared = response.headers.get("Content-Length")
                if declared and int(declared) > MAX_INPUT_BYTES:
                    raise ValueError(f"File exceeds the {_human_size(MAX_INPUT_BYTES)} input limit.")
                chunks = []
                total_bytes = 0
                while True:
                    chunk = response.read(128 * 1024)
                    if not chunk:
                        break
                    total_bytes += len(chunk)
                    if total_bytes > MAX_INPUT_BYTES:
                        raise ValueError(f"File exceeds the {_human_size(MAX_INPUT_BYTES)} input limit.")
                    chunks.append(chunk)
                body = b"".join(chunks)
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



_LOADER_URL_RE = re.compile(r"^/v1/(?:loaders|boot)/([A-Za-z0-9_-]+?)(?:\.lua)?/?$", re.IGNORECASE)


def _loader_boot_url(url: str) -> Optional[str]:
    """Loader links (…/v1/loaders/<id>.lua) resolve to their hidden boot route."""
    parsed = urllib.parse.urlparse((url or "").strip().strip("<>"))
    if parsed.scheme not in ("https", "http") or not parsed.hostname:
        return None
    match = _LOADER_URL_RE.match(urllib.parse.unquote(parsed.path))
    if not match:
        return None
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/v1/boot/%s.lua" % match.group(1), "", parsed.query, ""))


def _download_command_source(url: str, destination: Path) -> tuple[str, int, Optional[str]]:
    """Fetch a command's source. Loader links go through the boot chain so the
    real script is recovered instead of the decoy; raw links are fetched as-is."""
    boot = _loader_boot_url(url)
    if boot:
        try:
            filename, size, depth, note = _download_get_source(boot, destination)
            if note is None:
                note = ("Loader link resolved to the loader source itself; no followable script URL was found (the loader may be key-gated)."
                        if depth == 0 else
                        "Loader link resolved to the real script (%d hop(s) followed)." % depth)
            return filename, size, note
        except (ValueError, OSError):
            pass
    filename, size = _download_url(url, destination, allow_any_ext=True)
    return filename, size, None


async def _detect_scores(source_path: Path) -> tuple[list[tuple[str, float, str, list[str]]], str]:
    """Score every engine against the file:
    [(name, confidence, label, evidence), ...], best first."""
    try:
        returncode, stdout, stderr = await _run_process(
            [PYTHON, str(DEOB_SCRIPT), str(source_path), "--detect-all", "--no-pypy"],
            90,
        )
    except asyncio.TimeoutError:
        raise ValueError("The detection scan timed out.")
    except JobMemoryExceeded as exc:
        raise ValueError(f"The detection scan exceeded the memory budget ({exc}).") from exc
    except OSError as exc:
        raise ValueError(f"Could not start the detection scan: {exc}") from exc
    if returncode != 0:
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
    has_header_evidence = any(
        confidence >= 0.75 and any(
            marker in str(item).lower()
            for item in evidence
            for marker in ("header comment", "leading header", "vendor header", "official header", "header line")
        )
        for _name, confidence, _label, evidence in rows
    )
    if has_header_evidence:
        basis = "validated leading header comment + full-file code structure"
    else:
        basis = "comment-independent full-file code-structure analysis"
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


async def _run_process(args: list[str], timeout: int, env: Optional[dict[str, str]] = None) -> tuple[int, bytes, bytes]:
    global _active_jobs
    proc = await asyncio.create_subprocess_exec(
        *args, cwd=str(DEOB_DIR), env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
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
            await asyncio.sleep(1.0)
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


@bot.command(name="do", aliases=["deobf"])
async def deobfuscate_command(ctx: commands.Context, *, url: str = "") -> None:
    """The per-obfuscator deobfuscation engines were removed; detection and the Env Logger remain."""
    await ctx.reply(
        view=info_view(
            "Deobfuscation engines removed",
            "MonLua no longer runs the per-obfuscator deobfuscation engines.\n"
            "Use .detect or .d to identify the obfuscator.\n"
            "Use .l with the file to run it in the sandbox and record everything it does.",
        ),
        mention_author=False,
    )


@bot.command(name="get")
async def get_cmd(ctx: commands.Context, *, url: str = "") -> None:
    url = (url or "").strip().strip("<>").strip()
    attachments = ctx.message.attachments
    if attachments and url:
        await ctx.reply(view=info_view("Choose one source", "Attach one file or give a URL, not both."), mention_author=False)
        return
    if len(attachments) > 1:
        await ctx.reply(view=info_view("Single-file processing", "Attach one file per request."), mention_author=False)
        return
    attachment = attachments[0] if attachments else None
    if attachment is None and not url:
        await ctx.reply(view=info_view("Usage", ".get with a `.lua`, `.luau`, or `.txt` attachment, or `.get <url>` to fetch raw source or resolve a supported loadstring URL."), mention_author=False)
        return
    if attachment is not None:
        filename = Path(attachment.filename).name
        if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            await ctx.reply(view=error_view("Unsupported file type", "Use `.lua`, `.luau`, or `.txt`."), mention_author=False)
            return
        if attachment.size > MAX_INPUT_BYTES:
            await ctx.reply(view=error_view("Input too large", f"Maximum input size: {_human_size(MAX_INPUT_BYTES)}."), mention_author=False)
            return

    url = _command_input_url(url)
    if attachment is not None:
        status = await ctx.reply(view=info_view("⏳ Reading source", "Loading the attached file."), mention_author=False)
    else:
        status = await ctx.reply(view=info_view("⏳ Fetching source", "Checking the URL and resolving embedded links."), mention_author=False)
    temporary = Path(tempfile.gettempdir()) / f"get_{time.time_ns() % 10**10}.bin"
    try:
        if attachment is not None:
            await attachment.save(temporary)
            filename = Path(attachment.filename).name
            size = temporary.stat().st_size
            loader_depth, fetch_note = 0, None
        else:
            filename, size, loader_depth, fetch_note = await asyncio.to_thread(_download_get_source, url, temporary)
        safe_name = Path(filename).name or "raw.txt"
        allowed_names = (".txt", ".lua", ".luau", ".json", ".js", ".py", ".md", ".csv", ".xml", ".html", ".ini", ".cfg", ".yml", ".yaml", ".log")
        if not safe_name.lower().endswith(allowed_names):
            safe_name += ".txt"
        details = [f"**File** · `{safe_name[:120]}`", f"**Size** · {_human_size(size)}"]
        if loader_depth:
            details.append(f"Resolved {loader_depth} embedded loadstring loader(s).")
        if fetch_note:
            details.append(f"Note · {fetch_note}")
        details_text = "\n".join(details)
        upload_limit = int(getattr(ctx.guild, "filesize_limit", 8 * 1024 * 1024) or (8 * 1024 * 1024))

        # Every .get result gets an online copy on Rubis (Pastefy fallback), so
        # the card always carries Open/View-raw links no matter how it delivers.
        online = ("", "", "")
        if size:
            try:
                source_text = await asyncio.to_thread(temporary.read_text, encoding="utf-8-sig", errors="replace")
                online = await asyncio.to_thread(_upload_output, source_text.rstrip(), Path(filename).stem or "raw")
            except Exception as exc:
                print(f".get online upload failed: {type(exc).__name__}: {exc}", flush=True)
                online = ("", "", "")

        if size <= 1800:
            preview = await asyncio.to_thread(temporary.read_text, encoding="utf-8-sig", errors="replace")
            preview = preview[:1200].replace("```", "`\u200b``")
            body = details_text + "\n\n```text\n" + preview + "\n```"
            preview_view = info_view("Source preview", body)
            if online[1]:
                preview_view.children[0].add_item(_online_action_row(online))
            await status.edit(content=None, view=preview_view)
        elif size <= upload_limit:
            fetched_view = info_view("Source fetched", details_text + "\nThe complete file is attached below.")
            if online[1]:
                fetched_view.children[0].add_item(_online_action_row(online))
            await status.edit(content=None, view=fetched_view)
            # Components V2 messages only show attachments referenced by a File
            # component, so the download card carries one pointing at the upload.
            download_view = info_view("Download ready", "The file is attached.")
            if online[1]:
                download_view.children[0].add_item(_online_action_row(online))
            download_view.children[0].add_item(discord.ui.File(discord.UnfurledMediaItem(f"attachment://{safe_name}")))
            await ctx.send(view=download_view, file=discord.File(fp=str(temporary), filename=safe_name))
        else:
            if online[1]:
                fetched_view = info_view("Source fetched", details_text + "\n\nThe complete file is available online.")
                fetched_view.children[0].add_item(_online_action_row(online))
                await status.edit(content=None, view=fetched_view)
            else:
                await status.edit(content=None, view=error_view("Source exceeds the upload limit", "Too large to attach here, and the online upload did not accept it."))
    except Exception as exc:
        if _is_size_limit_error(exc):
            await status.edit(content=None, view=error_view("Input too large", str(exc)[:400]))
        else:
            await status.edit(content=None, view=error_view("Could not fetch source", f"{type(exc).__name__}: {str(exc)[:700]}"))
    finally:
        try:
            temporary.unlink()
        except OSError:
            pass

@bot.command(name="detect", aliases=["d"])
async def detect(ctx: commands.Context, *, url: str = "") -> None:
    attachments = ctx.message.attachments
    if attachments and url.strip():
        await ctx.reply(view=info_view("Choose one input", "Attach one source file or provide a raw-file URL, not both."), mention_author=False)
        return
    if len(attachments) > 1:
        await ctx.reply(view=info_view("Single-file processing", "Attach one file per request."), mention_author=False)
        return
    attachment = attachments[0] if attachments else None
    source_url = _command_input_url(url)
    if attachment is None and not source_url:
        await ctx.reply(view=info_view("Source file required", "Attach one `.lua`, `.luau`, or `.txt` file, or provide a direct raw-file URL.\n\nExample\n`.detect https://example.com/raw/script.lua`"), mention_author=False)
        return
    if attachment is not None:
        filename = Path(attachment.filename).name
        if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
            await ctx.reply(view=error_view("Unsupported file type", "Use `.lua`, `.luau`, or `.txt`."), mention_author=False)
            return
        if attachment.size > MAX_INPUT_BYTES:
            await ctx.reply(view=error_view("Input too large", f"Maximum input size: {_human_size(MAX_INPUT_BYTES)}."), mention_author=False)
            return
    else:
        try:
            source_url, filename = _validate_public_url(source_url, allow_any_ext=True)
        except ValueError as exc:
            await ctx.reply(view=error_view("Invalid source URL", str(exc)), mention_author=False)
            return
    with tempfile.TemporaryDirectory(prefix="detect_bot_") as temp:
        input_path = Path(temp) / filename
        try:
            if attachment is not None:
                await attachment.save(input_path)
            else:
                filename, _size, _fetch_note = await asyncio.to_thread(_download_command_source, source_url, input_path)
            size = input_path.stat().st_size
            if size == 0:
                await ctx.reply(view=error_view("Empty source file", "The file contains no data."), mention_author=False)
                return
            if size > LOCAL_INPUT_BYTES:
                await ctx.reply(view=error_view("Input too large", f"Maximum input size: {_human_size(LOCAL_INPUT_BYTES)}. Detection runs locally."), mention_author=False)
                return
            status = await ctx.reply(view=info_view("⏳ Analyzing source", f"**File** · `{filename[:64]}`\n**Size** · {_human_size(size)}\nComparing the source structure against supported engines."), mention_author=False)
            start_time = time.monotonic()
            try:
                async with job_slots:
                    rows, basis = await _detect_scores(input_path)
            except ValueError as exc:
                await status.edit(content=None, view=error_view("Detection scan failed", str(exc)[:900]))
                return
            elapsed_seconds = max(1, int(time.monotonic() - start_time))
            elapsed = f"{elapsed_seconds}s" if elapsed_seconds < 120 else f"{elapsed_seconds // 60}m {elapsed_seconds % 60}s"
            try:
                await status.edit(content=None, view=detect_view(filename, rows, basis, elapsed))
            except discord.HTTPException:
                best_label = rows[0][2] if rows else "nothing"
                best_pct = int(round(rows[0][1] * 100)) if rows else 0
                await status.edit(content=None, view=info_view("Detection result", f"**Best match** · {best_label}\n**Confidence** · {best_pct}%\nThe full report is not supported by this client.", color=0xFAA61A))
        except discord.HTTPException:
            print("Discord permission error during .detect: cannot read/send messages.", flush=True)


@bot.command(name="beautify", aliases=["b"])
async def beautify_command(ctx: commands.Context, *, source: str = "") -> None:
    attachments = ctx.message.attachments
    source_argument = (source or "").strip()
    if len(attachments) > 1:
        await ctx.reply(
            content="Single-file beautification\nAttach one .lua, .luau, or .txt file per request.",
            mention_author=False,
        )
        return
    if attachments and source_argument:
        await ctx.reply(
            content="Choose one source\nAttach one Lua file, provide a raw URL, or paste code into the command.",
            mention_author=False,
        )
        return
    if not attachments and not source_argument:
        await ctx.reply(
            content=(
                "Usage\n"
                ".beautify with a .lua or .luau attachment\n"
                ".beautify followed by a raw Lua URL\n"
                ".beautify followed by a Lua code block"
            ),
            mention_author=False,
        )
        return

    try:
        async with ctx.typing():
            if attachments:
                attachment = attachments[0]
                filename = Path(attachment.filename).name
                if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
                    raise ValueError("Supported attachment types are .lua, .luau, and .txt.")
                if attachment.size > MAX_FORMAT_BYTES:
                    raise ValueError(f"Source exceeds the {_human_size(MAX_FORMAT_BYTES)} beautification limit.")
                with tempfile.TemporaryDirectory(prefix="beautify_bot_") as directory:
                    input_path = Path(directory) / filename
                    await attachment.save(input_path)
                    source_bytes = await asyncio.to_thread(input_path.read_bytes)
                    source_text = source_bytes.decode("utf-8-sig")
            elif _looks_like_url_argument(source_argument):
                source_url = _command_input_url(source_argument)
                source_url, filename = _validate_public_url(source_url, allow_any_ext=True)
                with tempfile.TemporaryDirectory(prefix="beautify_bot_") as directory:
                    input_path = Path(directory) / "source.bin"
                    filename, _bsize, _bnote = await asyncio.to_thread(_download_command_source, source_url, input_path)
                    source_bytes = await asyncio.to_thread(input_path.read_bytes)
                    if len(source_bytes) > MAX_FORMAT_BYTES:
                        raise ValueError(f"Source exceeds the {_human_size(MAX_FORMAT_BYTES)} beautification limit.")
                    source_text = source_bytes.decode("utf-8-sig")
            else:
                filename = "pasted_code.lua"
                source_text = _unwrap_lua_code_block(source_argument)

            if len(source_text.encode("utf-8")) > MAX_FORMAT_BYTES:
                raise ValueError(f"Source exceeds the {_human_size(MAX_FORMAT_BYTES)} beautification limit.")
            formatted = await asyncio.to_thread(_beautify_source, source_text, filename)

        await _send_beautified_output(ctx, filename, formatted)
    except UnicodeDecodeError:
        await ctx.reply(
            content="Could not beautify this source\nThe file must use UTF-8 text encoding.",
            mention_author=False,
        )
    except ValueError as exc:
        await ctx.reply(content=f"Could not beautify this source\n{str(exc)[:900]}", mention_author=False)
    except RuntimeError as exc:
        await ctx.reply(content=f"Formatter unavailable\n{str(exc)[:900]}", mention_author=False)
    except discord.Forbidden:
        print("Discord permission error during .beautify: cannot read or send messages or attachments.", flush=True)
    except discord.HTTPException as exc:
        print(f"Discord error during .beautify: {type(exc).__name__}: {exc}", flush=True)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Unexpected .beautify error: {type(exc).__name__}: {exc}\n{traceback.format_exc()}", flush=True)
        try:
            await ctx.reply(
                content="Beautification failed\nAn unexpected error occurred. Check the bot service logs for details.",
                mention_author=False,
            )
        except discord.HTTPException:
            pass


def _env_logger_ready() -> bool:
    return (
        LUNE_BIN.is_file()
        and os.access(LUNE_BIN, os.X_OK)
        and ENVLOGGER_SCRIPT.is_file()
        and ENVLOGGER_APIDUMP.is_file()
    )


def _run_env_logger(input_path: Path, output_path: Path) -> tuple[int, str, str]:
    if not _env_logger_ready():
        raise RuntimeError("The Env Logger runtime is not installed in this deployment.")
    if not os.access(input_path, os.R_OK):
        raise RuntimeError("The source file could not be read back for logging.")
    proc = subprocess.run(
        [str(LUNE_BIN), "run", str(ENVLOGGER_SCRIPT), str(input_path), str(output_path)],
        capture_output=True,
        timeout=ENVLOGGER_TIMEOUT,
        cwd=str(ENVLOGGER_DIR),
    )
    return (
        proc.returncode,
        (proc.stdout or b"").decode("utf-8", "replace"),
        (proc.stderr or b"").decode("utf-8", "replace"),
    )


@bot.command(name="l", aliases=["envlog", "envlogger"])
async def env_logger_command(ctx: commands.Context, *, source: str = "") -> None:
    """Run the MonLua Env Logger on a Lua source and deliver the recorded trace."""
    attachments = ctx.message.attachments
    source_argument = (source or "").strip()
    if len(attachments) > 1:
        await ctx.reply(
            content="Single-file logging\nAttach one .lua, .luau, or .txt file per request.",
            mention_author=False,
        )
        return
    if attachments and source_argument:
        await ctx.reply(
            content="Choose one source\nAttach one Lua file, provide a raw URL, or paste code into the command.",
            mention_author=False,
        )
        return
    if not attachments and not source_argument:
        await ctx.reply(
            content=(
                "Usage\n"
                ".l with a .lua or .luau attachment\n"
                ".l followed by a raw Lua URL\n"
                ".l followed by a Lua code block"
            ),
            mention_author=False,
        )
        return

    status = await ctx.reply(
        view=info_view("⏳ Env Logger", "Running your script in a sandbox and recording everything it does."),
        mention_author=False,
    )
    try:
        async with ctx.typing():
            if attachments:
                attachment = attachments[0]
                filename = Path(attachment.filename).name
                if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
                    raise ValueError("Supported attachment types are .lua, .luau, and .txt.")
                if attachment.size > LOCAL_INPUT_BYTES:
                    raise ValueError(f"Source exceeds the {_human_size(LOCAL_INPUT_BYTES)} input limit (the Env Logger runs locally).")
            elif _looks_like_url_argument(source_argument):
                source_url = _command_input_url(source_argument)
                source_url, filename = _validate_public_url(source_url, allow_any_ext=True)
            else:
                filename = "pasted_code.lua"

            with tempfile.TemporaryDirectory(prefix="envlogger_bot_") as directory:
                input_path = Path(directory) / filename
                if attachments:
                    await attachment.save(input_path)
                    size = input_path.stat().st_size
                    if size == 0:
                        raise ValueError("The supplied file contains no data.")
                    if size > LOCAL_INPUT_BYTES:
                        raise ValueError(f"Source exceeds the {_human_size(LOCAL_INPUT_BYTES)} input limit (the Env Logger runs locally).")
                elif _looks_like_url_argument(source_argument):
                    saved_name, size, _note = await asyncio.to_thread(_download_command_source, source_url, input_path)
                    filename = saved_name or filename
                    if size > LOCAL_INPUT_BYTES:
                        raise ValueError(f"Source exceeds the {_human_size(LOCAL_INPUT_BYTES)} input limit (the Env Logger runs locally).")
                else:
                    source_text = _unwrap_lua_code_block(source_argument)
                    input_path.write_text(source_text, encoding="utf-8")

                started = time.monotonic()
                returncode, stdout_text, stderr_text = await asyncio.to_thread(
                    _run_env_logger, input_path, Path(directory) / "dump_out.lua"
                )
                elapsed = f"{time.monotonic() - started:.1f}s"
                output_path = Path(directory) / "dump_out.lua"
                if not output_path.exists() or output_path.stat().st_size == 0:
                    detail = (stderr_text or stdout_text or "").strip()[-700:] or "no diagnostic output"
                    raise RuntimeError(f"The Env Logger run failed: {detail}")

                raw_dump = await asyncio.to_thread(output_path.read_text, encoding="utf-8", errors="replace")
                final_text = await asyncio.to_thread(_finish_output, raw_dump, "-- Deobfuscated by MonLua [discord.gg/EdrQjndmAW]")
                notes = stdout_text.strip()
                if notes:
                    final_text += "\n-- [Env Logger notes]\n" + notes[:1200] + "\n"
                output_path = Path(directory) / f"envlog_{Path(filename).stem}.lua"
                await asyncio.to_thread(output_path.write_text, final_text, encoding="utf-8", newline="\n")
                out_text = final_text
                output_size = output_path.stat().st_size

        delivered = await _deliver_deobf_output(
            ctx,
            status,
            filename,
            "Env Logger",
            output_path,
            output_size,
            out_text,
            elapsed,
        )
        if not delivered:
            raise RuntimeError("The logged output could not be delivered.")
    except subprocess.TimeoutExpired:
        await status.edit(content=None, view=error_view("Env Logger", f"The run exceeded the {ENVLOGGER_TIMEOUT}s limit."))
    except ValueError as exc:
        await status.edit(content=None, view=error_view("Env Logger", str(exc)[:900]))
    except RuntimeError as exc:
        await status.edit(content=None, view=error_view("Env Logger", str(exc)[:900]))
    except discord.Forbidden:
        print("Discord permission error during .l: cannot read or send messages or attachments.", flush=True)
    except discord.HTTPException as exc:
        print(f"Discord error during .l: {type(exc).__name__}: {exc}", flush=True)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print(f"Unexpected .l error: {type(exc).__name__}: {exc}\n{traceback.format_exc()}", flush=True)
        try:
            await status.edit(content=None, view=error_view("Env Logger", "An unexpected error occurred. Check the service logs."))
        except discord.HTTPException:
            pass


@bot.command(name="deobfs", aliases=["deobfuscators", "engines"])
async def deobfs(ctx: commands.Context) -> None:
    await ctx.reply(view=info_view("MonLua engines", engines_body()), mention_author=False)


@bot.command(name="help")
async def help_command(ctx: commands.Context) -> None:
    body = (
        engines_body()
        + "\n\n**INPUT EXAMPLES**\n"
        + "• `.detect` or `.d` with a file attached\n"
        + "• `.beautify` or `.b` followed by a raw Lua URL or pasted code\n"
        + "• `.l` with a Lua file attached (Env Logger: records remotes, strings, globals and actions in a sandbox)\n"
        + "• `.get <url>` to fetch raw source or resolve embedded loaders"
    )
    await ctx.reply(view=info_view("GUIDE COMMANDS", body), mention_author=False)


_tree_synced = False


set_group = app_commands.Group(
    name="set",
    description="Configure MonLua for this server.",
    guild_only=True,
)


@set_group.command(name="channel", description="Allow bot commands only in this channel (add it to the allowlist).")
@app_commands.describe(channel="Text channel where bot commands are allowed.")
async def set_channel_command(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    global CHANNEL_CONFIG_LOAD_FAILED
    member = interaction.user
    permissions = getattr(member, "guild_permissions", None)
    if interaction.guild_id is None:
        await interaction.response.send_message(view=error_view("Server only", "Use this in a server."), ephemeral=True)
        return
    if not permissions or not (permissions.manage_guild or permissions.administrator):
        await interaction.response.send_message(view=error_view("Permission required", "Manage Server or Administrator permission required."), ephemeral=True)
        return
    guild = interaction.guild
    if channel.guild.id != interaction.guild_id:
        await interaction.response.send_message(view=error_view("Invalid channel", "Choose a text channel from this server."), ephemeral=True)
        return
    guild_key = str(interaction.guild_id)
    async with _channel_settings_lock:
        updated = {key: list(value) for key, value in CHANNEL_RESTRICTIONS.items()}
        current = set(updated.get(guild_key, []))
        # Deleted channels must not ride along in the saved allowlist.
        pruned = {cid for cid in current if guild.get_channel(cid) is None}
        current -= pruned
        if guild.get_channel(channel.id) is None:
            # The picked channel itself no longer exists: save nothing, just clean up.
            updated[guild_key] = sorted(current)
            if not updated[guild_key]:
                updated.pop(guild_key, None)
            try:
                _persist_channel_restrictions(updated)
            except OSError as exc:
                print(f"Couldn't persist channel restriction: {type(exc).__name__}: {exc}", flush=True)
                await interaction.response.send_message(view=error_view("Could not save setting", "Check the bot file permissions and try again."), ephemeral=True)
                return
            CHANNEL_RESTRICTIONS.clear()
            CHANNEL_RESTRICTIONS.update(updated)
            CHANNEL_CONFIG_LOAD_FAILED = False
            cleaned = f" Cleaned {len(pruned)} deleted channel(s) from the saved list." if pruned else ""
            await interaction.response.send_message(view=error_view("Channel no longer exists", f"{channel.mention} was deleted, so it was not saved.{cleaned}"), ephemeral=True)
            return
        current.add(channel.id)
        updated[guild_key] = sorted(current)
        try:
            _persist_channel_restrictions(updated)
        except OSError as exc:
            print(f"Couldn't persist channel restriction: {type(exc).__name__}: {exc}", flush=True)
            await interaction.response.send_message(view=error_view("Could not save setting", "Check the bot file permissions and try again."), ephemeral=True)
            return
        CHANNEL_RESTRICTIONS.clear()
        CHANNEL_RESTRICTIONS.update(updated)
        CHANNEL_CONFIG_LOAD_FAILED = False
        configured_count = len(updated[guild_key])
        pruned_count = len(pruned)
    suffix = (f" Cleaned {pruned_count} deleted channel(s) from the saved list." if pruned_count else "")
    await interaction.response.send_message(view=info_view("Command channel saved", f"Commands now allowed in {channel.mention}" + (f" and {configured_count - 1} more." if configured_count > 1 else ".") + "\nRun /set channel for another." + suffix, color=0x57F287), ephemeral=True)
    _schedule_channel_backup()



remove_group = app_commands.Group(
    name="remove",
    description="Remove MonLua configuration.",
    guild_only=True,
)
remove_set_group = app_commands.Group(
    name="set",
    description="Remove a setting.",
    guild_only=True,
)


@remove_set_group.command(name="channel", description="Remove a channel from the bot-command allowlist.")
@app_commands.describe(channel="Previously configured text channel to remove.")
async def remove_set_channel_command(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    global CHANNEL_CONFIG_LOAD_FAILED
    member = interaction.user
    permissions = getattr(member, "guild_permissions", None)
    if interaction.guild_id is None:
        await interaction.response.send_message(view=error_view("Server only", "Use this in a server."), ephemeral=True)
        return
    if not permissions or not (permissions.manage_guild or permissions.administrator):
        await interaction.response.send_message(view=error_view("Permission required", "Manage Server or Administrator permission required."), ephemeral=True)
        return
    guild = interaction.guild
    guild_key = str(interaction.guild_id)
    async with _channel_settings_lock:
        updated = {key: list(value) for key, value in CHANNEL_RESTRICTIONS.items()}
        current = set(updated.get(guild_key, []))
        # Deleted channels must not ride along in the saved allowlist.
        pruned = {cid for cid in current if guild.get_channel(cid) is None}
        current -= pruned
        if channel.id not in current:
            if channel.id in pruned:
                # The channel was already deleted from Discord; finish removing it from the saved list.
                if current:
                    updated[guild_key] = sorted(current)
                else:
                    updated.pop(guild_key, None)
                try:
                    _persist_channel_restrictions(updated)
                except OSError as exc:
                    print(f"Couldn't persist channel restriction removal: {type(exc).__name__}: {exc}", flush=True)
                    await interaction.response.send_message(view=error_view("Could not save change", "The existing channel restriction is still active."), ephemeral=True)
                    return
                CHANNEL_RESTRICTIONS.clear()
                CHANNEL_RESTRICTIONS.update(updated)
                CHANNEL_CONFIG_LOAD_FAILED = False
                extra = f" Also cleaned {len(pruned) - 1} other deleted channel(s)." if len(pruned) > 1 else ""
                await interaction.response.send_message(view=info_view("Channel cleaned", f"{channel.mention} was deleted. Removed it from the saved list.{extra}", color=0x57F287), ephemeral=True)
                _schedule_channel_backup()
            else:
                await interaction.response.send_message(view=info_view("Channel not configured", f"{channel.mention} is not configured here."), ephemeral=True)
            return
        current.remove(channel.id)
        if current:
            updated[guild_key] = sorted(current)
        else:
            updated.pop(guild_key, None)
        try:
            _persist_channel_restrictions(updated)
        except OSError as exc:
            print(f"Couldn't persist channel restriction removal: {type(exc).__name__}: {exc}", flush=True)
            await interaction.response.send_message(view=error_view("Could not save change", "The existing channel restriction is still active."), ephemeral=True)
            return
        CHANNEL_RESTRICTIONS.clear()
        CHANNEL_RESTRICTIONS.update(updated)
        CHANNEL_CONFIG_LOAD_FAILED = False
        remaining = len(current)
        pruned_count = len(pruned)
    if remaining:
        message = f"Removed {channel.mention}. Commands remain restricted to the other {remaining} configured channel(s)."
    else:
        message = f"Removed {channel.mention}. This server no longer has a command-channel restriction."
    if pruned_count:
        message += f" Also cleaned {pruned_count} deleted channel(s) from the saved list."
    await interaction.response.send_message(view=info_view("Command channel updated", message, color=0x57F287), ephemeral=True)
    _schedule_channel_backup()



remove_group.add_command(remove_set_group)
bot.tree.add_command(set_group)
bot.tree.add_command(remove_group)


@bot.event
async def on_ready() -> None:
    await _restore_channel_restrictions_remote()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)
    if _env_logger_ready():
        print("Env Logger runtime ready.", flush=True)
    else:
        print("WARNING: Env Logger runtime missing or not executable.", flush=True)
    global _tree_synced
    if not _tree_synced:
        try:
            synced = await bot.tree.sync()
            _tree_synced = True
            print(f"Synced {len(synced)} Discord application command(s).", flush=True)
        except (discord.HTTPException, app_commands.AppCommandError) as exc:
            print(f"WARNING: slash-command sync failed: {type(exc).__name__}: {exc}", flush=True)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, ChannelRestrictionCheckFailure):
        configured = _allowed_channel_ids(ctx.guild.id if ctx.guild else None)
        details = "Bot commands are restricted to the configured channel list."
        if configured:
            details += "\nAllowed channels: " + ", ".join(f"<#{channel_id}>" for channel_id in configured)
        try:
            await ctx.reply(view=info_view("Command unavailable here", details), mention_author=False)
        except discord.HTTPException:
            pass
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(view=info_view("Command cooldown", "Please wait a moment before trying again."), mention_author=False)
        return
    original = getattr(error, "original", error)
    print(f"Command error: {type(original).__name__}: {original}", flush=True)
    if _is_size_limit_error(original):
        try:
            await ctx.reply(view=error_view("Input too large", str(original)[:400]), mention_author=False)
        except discord.HTTPException:
            pass
        return
    try:
        await ctx.reply(view=error_view("Command failed", "Something went wrong. Check the service logs."), mention_author=False)
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
