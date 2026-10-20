from __future__ import annotations

import asyncio
import html
import ipaddress
import json
import os
import re
import shutil
import tarfile
import time
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands

ROOT = Path(__file__).resolve().parent
DEOB_DIR = ROOT / "deobf"
DEOB_SCRIPT = DEOB_DIR / "deob.py"
PYTHON = os.getenv("PYTHON", sys.executable or "python3")
MAX_INPUT_BYTES = max(1, int(os.getenv("MAX_INPUT_BYTES", str(8 * 1024 * 1024))))
MAX_OUTPUT_BYTES = max(1, int(os.getenv("MAX_OUTPUT_BYTES", str(24 * 1024 * 1024))))
JOB_TIMEOUT = max(10, min(600, int(os.getenv("DEOB_TIMEOUT", "600"))))
MAX_CONCURRENT_JOBS = max(1, int(os.getenv("MAX_CONCURRENT_JOBS", "2")))
URL_TIMEOUT = max(5, min(45, int(os.getenv("URL_TIMEOUT", "20"))))
ALLOWED_EXTENSIONS = {".lua", ".luau", ".txt"}
SUPPORTED = {
    "luraph_v15": {"label": "Luraph v15", "command": ".lph15"},
    "luraph_v151": {"label": "Luraph v15.1", "command": ".lph15.1"},
    "ironbrew1": {"label": "IronBrew1", "command": ".ibrw"},
    "moonsec_v3": {"label": "MoonSec V3", "command": ".moonv3"},
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


def info_view(title: str, body: str, color: int = 0x5865F2) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=color)
    container.add_item(discord.ui.TextDisplay(f"## {title}"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(body))
    view.add_item(container)
    return view


def engines_body() -> str:
    return (
        "**Luraph v15.1** \u2014 `.lph15.1`\n"
        "**Luraph v15** \u2014 `.lph15`\n"
        "**IronBrew1** \u2014 `.ibrw`\n"
        "**MoonSec V3** \u2014 `.moonv3`\n\n"
        "Attach one `.lua`, `.luau`, or `.txt` file with the command, or pass a direct raw-file URL.\n"
        "Every file is scanned first: the command only runs when the detected engine matches.\n\n"
        "-# `.deobfs` / `.engines` \u2014 engines \u00b7 `.help` \u2014 usage"
    )


def result_view(filename: str, label: str, size: int, code_text, file_name, elapsed: str = "") -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=0x57F287)
    container.add_item(discord.ui.TextDisplay("## \u2705 Deobfuscation complete"))
    container.add_item(discord.ui.TextDisplay(f"**File:** `{filename}`"))
    container.add_item(discord.ui.Separator())
    if code_text is not None:
        container.add_item(discord.ui.TextDisplay(f"```lua\n{code_text}\n```"))
    if file_name is not None:
        container.add_item(discord.ui.File(discord.UnfurledMediaItem(f"attachment://{file_name}")))
        container.add_item(discord.ui.TextDisplay("**Output:** attached above \u2b06"))
    container.add_item(discord.ui.Separator())
    stats = f"-# \u2699\ufe0f Engine **{label}** \u00b7 \U0001f4e6 {size:,} bytes"
    if elapsed:
        stats += f" \u00b7 \u23f1\ufe0f {elapsed}"
    stats += " \u00b7 \u26a0\ufe0f Review before running"
    container.add_item(discord.ui.TextDisplay(stats))
    view.add_item(container)
    return view


def error_view(title: str, detail: str) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=0xED4245)
    container.add_item(discord.ui.TextDisplay(f"## \u274c {title}"))
    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(f"```text\n{detail}\n```"))
    container.add_item(discord.ui.TextDisplay("-# \U0001f4a1 `.help` lists the supported engines and file types"))
    view.add_item(container)
    return view


def runtime_status() -> tuple[bool, str]:
    suffix = ".exe" if os.name == "nt" else ""
    required = (DEOB_DIR / "bin" / f"luau{suffix}", DEOB_DIR / "bin" / f"luau-ast{suffix}", DEOB_SCRIPT)
    missing = [str(p) for p in required if not p.is_file() or (os.name != "nt" and not os.access(p, os.X_OK))]
    return (not missing, ", ".join(missing) if missing else ", ".join(map(str, required)))


def _validate_public_url(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url.strip().strip("<>"))
    if parsed.scheme not in ("https", "http") or not parsed.hostname:
        raise ValueError("Please provide a direct HTTP(S) raw-file URL.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing embedded credentials are not accepted.")
    filename = Path(urllib.parse.unquote(parsed.path)).name
    suffix = Path(filename).suffix.lower()
    if not filename or (suffix and suffix not in ALLOWED_EXTENSIONS):
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


def _download_url(url: str, destination: Path) -> tuple[str, int]:
    current_url = url
    opener = urllib.request.build_opener(_NoRedirect)
    for _ in range(4):
        current_url, filename = _validate_public_url(current_url)
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
                refused = exc
                if exc.code in (401, 403, 406, 418, 429):
                    continue
                raise ValueError(f"Could not download the raw file (HTTP {exc.code}).") from exc
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                raise ValueError("Could not download that raw URL. Make sure it is publicly accessible.") from exc
        if response is None:
            code = refused.code if refused is not None else 0
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
    raise ValueError("Too many redirects while downloading the raw file.")


async def _scan_engine(source_path: Path) -> tuple[Optional[str], str]:
    try:
        proc = await asyncio.create_subprocess_exec(
            PYTHON, str(DEOB_SCRIPT), str(source_path), "--detect", "--no-pypy",
            cwd=str(DEOB_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
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


async def _run_process(args: list[str], timeout: int) -> tuple[int, bytes, bytes]:
    proc = await asyncio.create_subprocess_exec(
        *args, cwd=str(DEOB_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        if proc.returncode is None:
            proc.kill()
        await proc.communicate()
        raise
    return proc.returncode or 0, stdout, stderr


def result_embed(filename: str, label: str, size: int, desc: str, file_note: bool) -> discord.Embed:
    embed = discord.Embed(title=filename, color=0x57F287, description=desc[:4000])
    embed.add_field(name="Engine", value=label, inline=True)
    embed.add_field(name="Size", value=f"{size:,} bytes", inline=True)
    embed.set_footer(text="Output attached." if file_note else "Review before running.")
    return embed


async def process_input(ctx: commands.Context, engine: str, url: str = "") -> None:
    spec = SUPPORTED[engine]
    label = spec["label"]
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
            f"Use `{spec['command']}` with one `.lua`, `.luau`, or `.txt` attachment, or a direct raw-file URL.\n"
            f"Example: `{spec['command']} https://example.com/raw/script.lua`",
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
                if attachment is not None:
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
                    await status.edit(content=(
                        f"❓ Couldn't identify the obfuscator in `{filename}`.\nSupported: **Luraph v15/v15.1**, **IronBrew1**, **MoonSec V3**.\n`{diagnostic[:200]}`"
                    ))
                    return
                if detected != engine and not (engine == "luraph_v151" and detected == "luraph_v15"):
                    detected_label = SUPPORTED[detected]["label"]
                    await status.edit(content=(
                        f"That file is **{detected_label}**. Use `{SUPPORTED[detected]['command']}` instead."
                    ))
                    return

                wait_note = " This engine can take a few minutes on bigger files." if engine == "luraph_v151" else ""
                await status.edit(content=f"⚙️ Detected **{label}**. Devirtualizing `{filename}`…{wait_note}")
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
                    command = [node_bin, str(V151_SCRIPT), str(node_input), "-o", str(output_path), "--timeout", "150"]
                else:
                    command = [PYTHON, str(DEOB_SCRIPT), str(input_path), "--obfuscator", engine,
                               "--output", str(output_path), "--timeout", str(JOB_TIMEOUT), "--no-pypy"]
                try:
                    returncode, stdout, stderr = await _run_process(command, JOB_TIMEOUT + 15)
                except asyncio.TimeoutError:
                    await status.edit(content=f"⏱️ Timed out processing `{filename}` after {JOB_TIMEOUT} seconds.")
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

                out_text = output_path.read_text(encoding="utf-8", errors="replace")
                if engine == "luraph_v151" and not out_text.startswith("-- [[ Deobfuscated by MonLua ]]"):
                    out_text = "-- [[ Deobfuscated by MonLua ]]\n\n" + out_text.lstrip("\ufeff")
                    output_path.write_text(out_text, encoding="utf-8")
                output_size = output_path.stat().st_size
                if output_size > MAX_OUTPUT_BYTES:
                    await status.edit(content=f"📦 Output too large: {output_size:,} bytes (limit {MAX_OUTPUT_BYTES:,}).")
                    return
                elapsed_seconds = max(1, int(time.monotonic() - start_time))
                elapsed = f"{elapsed_seconds}s" if elapsed_seconds < 120 else f"{elapsed_seconds // 60}m {elapsed_seconds % 60}s"
                await status.edit(content=f"✅ Deobfuscated `{filename}` with **{label}**.")
                if output_size <= 1600 and "```" not in out_text:
                    await ctx.reply(view=result_view(filename, label, output_size, out_text.rstrip(), None, elapsed), mention_author=False)
                else:
                    await ctx.reply(
                        view=result_view(filename, label, output_size, None, output_path.name, elapsed),
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


@bot.command(name="lph15")
async def lph15(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "luraph_v15", url)


@bot.command(name="lph15.1")
async def lph15_1(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "luraph_v151", url)


@bot.command(name="ibrw")
async def ibrw(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "ironbrew1", url)


@bot.command(name="moonv3")
async def moonv3(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "moonsec_v3", url)


@bot.command(name="deobfs", aliases=["deobfuscators", "engines"])
async def deobfs(ctx: commands.Context) -> None:
    await ctx.reply(view=info_view("Supported deobfuscators", engines_body()), mention_author=False)


@bot.command(name="help")
async def help_command(ctx: commands.Context) -> None:
    body = engines_body() + (
        "\n\nAttach one source file or give a direct raw-file URL. "
        "Examples: `.lph15.1 https://host/path/script.lua`, or `.moonv3` with a file attached."
    )
    await ctx.reply(view=info_view("How to use MonLua", body), mention_author=False)


@bot.event
async def on_ready() -> None:
    ok, detail = runtime_status()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)
    if ok:
        print(f"Native runtimes found: {detail}", flush=True)
    else:
        print(f"WARNING: native runtimes missing or not executable: {detail}", flush=True)
    if not (V151_SCRIPT.is_file() and V151_NODE_ARCHIVE.is_file()):
        print("WARNING: v15.1 runtime incomplete; .lph15.1 will be unavailable.", flush=True)


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
