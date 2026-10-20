from __future__ import annotations

import asyncio
import html
import ipaddress
import json
import os
import re
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
    "ironbrew1": {"label": "IronBrew1", "command": ".ibrw"},
    "moonsec_v3": {"label": "MoonSec V3", "command": ".moonv3"},
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
job_slots = asyncio.Semaphore(MAX_CONCURRENT_JOBS)


def supported_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Supported deobfuscators",
        description=(
            "The bot scans the source first. It only processes a file when the detected "
            "obfuscator matches the command used."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Luraph v15 — `.lph15`", value="Accepts one `.lua`, `.luau`, or `.txt` attachment or raw-file URL.", inline=False)
    embed.add_field(name="IronBrew1 — `.ibrw`", value="Accepts one `.lua`, `.luau`, or `.txt` attachment or raw-file URL.", inline=False)
    embed.add_field(name="Input rules", value="No other file extensions, web pages, or generic/unknown obfuscators are accepted.", inline=False)
    embed.add_field(name="Other commands", value="`.deobfs` / `.engines` — list engines\n`.help` — usage", inline=False)
    return embed


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

                status = await ctx.reply(f"Scanning `{filename}` to identify its obfuscator…", mention_author=False)
                detected, diagnostic = await _scan_engine(input_path)
                if detected is None:
                    await status.edit(content=(
                        f"Unsupported obfuscator for `{filename}`. This bot only supports **Luraph v15**, **IronBrew1**, and **MoonSec V3**. "
                        f"Your file was not processed.\n`{diagnostic[:500]}`"
                    ))
                    return
                if detected != engine:
                    detected_label = SUPPORTED[detected]["label"]
                    await status.edit(content=(
                        f"Command mismatch: this file was detected as **{detected_label}**, but you used `{spec['command']}`. "
                        f"Nothing was deobfuscated. Use `{SUPPORTED[detected]['command']}` instead."
                    ))
                    return

                await status.edit(content=f"{diagnostic} Processing `{filename}` with **{label}**…")
                command = [PYTHON, str(DEOB_SCRIPT), str(input_path), "--obfuscator", engine,
                           "--output", str(output_path), "--timeout", str(JOB_TIMEOUT), "--no-pypy"]
                try:
                    returncode, stdout, stderr = await _run_process(command, JOB_TIMEOUT + 15)
                except asyncio.TimeoutError:
                    await status.edit(content=f"Timed out while processing `{filename}` after {JOB_TIMEOUT} seconds.")
                    return

                if returncode != 0 or not output_path.is_file() or output_path.stat().st_size == 0:
                    detail = (stderr or stdout).decode("utf-8", errors="replace").strip()
                    await status.edit(content=(
                        f"The file was identified as **{label}**, but deobfuscation failed. This version or script structure "
                        f"may not be supported.\n```text\n{detail[-800:] or 'No diagnostic output.'}\n```"
                    )[:1900])
                    print(f"Deobfuscation failed ({label}, {filename}): {detail[-2000:]}", flush=True)
                    return

                output_size = output_path.stat().st_size
                if output_size > MAX_OUTPUT_BYTES:
                    await status.edit(content=f"Output is too large ({output_size:,} bytes); limit is {MAX_OUTPUT_BYTES:,} bytes.")
                    return
                await status.edit(content=f"Successfully processed `{filename}` with **{label}**. Review the output before running it.")
                await ctx.reply(content=f"Deobfuscated output for `{filename}`:", file=discord.File(str(output_path), filename=output_path.name), mention_author=False)
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


@bot.command(name="ibrw")
async def ibrw(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "ironbrew1", url)


@bot.command(name="moonv3")
async def moonv3(ctx: commands.Context, *, url: str = "") -> None:
    await process_input(ctx, "moonsec_v3", url)


@bot.command(name="deobfs", aliases=["deobfuscators", "engines"])
async def deobfs(ctx: commands.Context) -> None:
    await ctx.reply(embed=supported_embed(), mention_author=False)


@bot.command(name="help")
async def help_command(ctx: commands.Context) -> None:
    embed = supported_embed()
    embed.description = (
        "Attach one source file or provide a direct raw-file URL. The bot scans the source first and rejects "
        "unsupported engines or commands that do not match the detected engine.\n\n"
        "Examples: `.lph15 https://host/path/script.lua` or `.ibrw` with a file attached."
    )
    await ctx.reply(embed=embed, mention_author=False)


@bot.event
async def on_ready() -> None:
    ok, detail = runtime_status()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)
    if ok:
        print(f"Native runtimes found: {detail}", flush=True)
    else:
        print(f"WARNING: native runtimes missing or not executable: {detail}", flush=True)


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
