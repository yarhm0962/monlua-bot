"""Discord bot for the bundled Lua/Luau deobfuscators.

Render deployment: run this as a Background Worker with `python bot.py`.
Required environment variable: DISCORD_BOT_TOKEN.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands

ROOT = Path(__file__).resolve().parent
DEOB_DIR = ROOT / "deobf"
DEOB_SCRIPT = DEOB_DIR / "deob.py"

MAX_INPUT_BYTES = max(1, int(os.getenv("MAX_INPUT_BYTES", str(8 * 1024 * 1024))))
MAX_OUTPUT_BYTES = max(1, int(os.getenv("MAX_OUTPUT_BYTES", str(24 * 1024 * 1024))))
JOB_TIMEOUT = max(10, min(600, int(os.getenv("DEOB_TIMEOUT", "600"))))
MAX_CONCURRENT_JOBS = max(1, int(os.getenv("MAX_CONCURRENT_JOBS", "2")))
PYTHON = os.getenv("PYTHON", sys.executable or "python3")

SUPPORTED = (
    {
        "label": "Luraph v15",
        "command": ".lph15",
        "engine": "luraph_v15",
        "description": "Luraph v15 devirtualizer with a behaviour-trace fallback.",
    },
    {
        "label": "IronBrew1",
        "command": ".ibrw",
        "engine": "ironbrew1",
        "description": "IronBrew1 devirtualizer with a behaviour-trace fallback for supported Luau variants.",
    },
    {
        "label": "Generic fallback",
        "command": "automatic",
        "engine": "generic",
        "description": "Generic behaviour-trace fallback; not a separate specialized VM deobfuscator.",
    },
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
job_slots = asyncio.Semaphore(MAX_CONCURRENT_JOBS)


def supported_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Available deobfuscators",
        description="Attach a `.lua`, `.luau`, or `.txt` file to the matching command.",
        color=discord.Color.blurple(),
    )
    for engine in SUPPORTED:
        embed.add_field(
            name=f"{engine['label']} — `{engine['command']}`",
            value=engine["description"],
            inline=False,
        )
    embed.add_field(
        name="Commands",
        value=(
            "`.lph15` — process a Luraph v15 script\n"
            "`.ibrw` — process an IronBrew1 script\n"
            "`.deobfs` — list all engines\n"
            "`.help` — show command help"
        ),
        inline=False,
    )
    embed.set_footer(text="Results are best-effort. Review generated code before running it.")
    return embed


def runtime_status() -> tuple[bool, str]:
    """Check every native executable required by the bundled deobfuscators."""
    suffix = ".exe" if os.name == "nt" else ""
    required = (DEOB_DIR / "bin" / f"luau{suffix}", DEOB_DIR / "bin" / f"luau-ast{suffix}")
    missing = [str(path) for path in required if not path.is_file() or (os.name != "nt" and not os.access(path, os.X_OK))]
    if missing:
        return False, ", ".join(missing)
    return True, ", ".join(str(path) for path in required)


@bot.event
async def on_ready() -> None:
    ready, binary = runtime_status()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)
    if ready:
        print(f"Luau runtime found: {binary}", flush=True)
    else:
        print(
            f"WARNING: required runtime tools are missing or not executable: {binary}. "
            "Both luau and luau-ast are required; see the deobfuscator setup notes.",
            flush=True,
        )


async def deobfuscate_attachment(
    ctx: commands.Context,
    attachment: Optional[discord.Attachment],
    engine: str,
) -> None:
    command_name = ".lph15" if engine == "luraph_v15" else ".ibrw"
    label = "Luraph v15" if engine == "luraph_v15" else "IronBrew1"

    if attachment is None:
        await ctx.reply(
            f"Attach a `.lua`, `.luau`, or `.txt` file to your message and use `{command_name}`.",
            mention_author=False,
        )
        return

    filename = Path(attachment.filename).name
    if Path(filename).suffix.lower() not in {".lua", ".luau", ".txt"}:
        await ctx.reply("Unsupported file type. Please attach a `.lua`, `.luau`, or `.txt` file.", mention_author=False)
        return
    if attachment.size > MAX_INPUT_BYTES:
        await ctx.reply(
            f"File is too large ({attachment.size:,} bytes). The configured limit is {MAX_INPUT_BYTES:,} bytes.",
            mention_author=False,
        )
        return

    runtime_ok, runtime_path = runtime_status()
    if not runtime_ok:
        await ctx.reply(
            "The bot is online, but required native runtime tools are missing or not executable: "
            f"`{runtime_path}`. The deobfuscator needs both `deobf/bin/luau` and "
            "`deobf/bin/luau-ast`; building only `luau` is not enough. Check the Render build logs.",
            mention_author=False,
        )
        print(f"Missing Luau runtime: {runtime_path}", flush=True)
        return

    async with job_slots:
        with tempfile.TemporaryDirectory(prefix="deobf_bot_") as temp_dir:
            workdir = Path(temp_dir)
            input_path = workdir / filename
            output_path = workdir / f"{Path(filename).stem}_deobfuscated.luau"
            status: Optional[discord.Message] = None
            proc: Optional[asyncio.subprocess.Process] = None

            try:
                await attachment.save(input_path)
                actual_size = input_path.stat().st_size
                if actual_size == 0:
                    await ctx.reply("That file is empty.", mention_author=False)
                    return
                if actual_size > MAX_INPUT_BYTES:
                    await ctx.reply("The downloaded file exceeds the configured input limit.", mention_author=False)
                    return

                status = await ctx.reply(f"Processing `{filename}` with **{label}**…", mention_author=False)
                command = [
                    PYTHON,
                    str(DEOB_SCRIPT),
                    str(input_path),
                    "--obfuscator", engine,
                    "--output", str(output_path),
                    "--timeout", str(JOB_TIMEOUT),
                    "--no-pypy",
                ]
                proc = await asyncio.create_subprocess_exec(
                    *command,
                    cwd=str(DEOB_DIR),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                try:
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=JOB_TIMEOUT + 15)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.communicate()
                    await status.edit(content=f"Timed out while processing `{filename}` after {JOB_TIMEOUT} seconds.")
                    return

                if proc.returncode != 0 or not output_path.is_file() or output_path.stat().st_size == 0:
                    detail = (stderr or stdout).decode("utf-8", errors="replace").strip()
                    message = f"Could not deobfuscate `{filename}` with **{label}**. This script variant may not be supported."
                    if detail:
                        # Keep diagnostic text short enough for Discord and avoid sending huge logs.
                        message += f"\n```text\n{detail[-1000:]}\n```"
                    await status.edit(content=message[:1900])
                    print(f"Job failed ({label}, {filename}): {detail[-2000:]}", flush=True)
                    return

                output_size = output_path.stat().st_size
                if output_size > MAX_OUTPUT_BYTES:
                    await status.edit(
                        content=(
                            f"Processing completed, but the output is {output_size:,} bytes, above the configured "
                            f"upload limit of {MAX_OUTPUT_BYTES:,} bytes."
                        )
                    )
                    return

                await status.edit(
                    content=f"Finished `{filename}` using **{label}**. The result is best-effort; review it before running."
                )
                await ctx.reply(
                    content=f"Deobfuscated output for `{filename}`:",
                    file=discord.File(str(output_path), filename=output_path.name),
                    mention_author=False,
                )

            except discord.Forbidden:
                print("Discord permission error: bot cannot read or send messages/files in this channel.", flush=True)
            except discord.HTTPException as exc:
                message = f"Discord upload/download error: {exc}"
                if status is not None:
                    try:
                        await status.edit(content=message[:1900])
                    except discord.HTTPException:
                        pass
                else:
                    await ctx.reply(message[:1900], mention_author=False)
            except asyncio.CancelledError:
                if proc is not None and proc.returncode is None:
                    proc.kill()
                    await proc.wait()
                raise
            except Exception as exc:
                print(f"Unexpected job error: {type(exc).__name__}: {exc}", flush=True)
                message = f"Unexpected processing error: `{type(exc).__name__}`. Check the Render logs for details."
                if status is not None:
                    try:
                        await status.edit(content=message)
                    except discord.HTTPException:
                        pass
                else:
                    await ctx.reply(message, mention_author=False)


@bot.command(name="lph15")
async def lph15(ctx: commands.Context, *, _unused: str = "") -> None:
    attachment = ctx.message.attachments[0] if ctx.message.attachments else None
    await deobfuscate_attachment(ctx, attachment, "luraph_v15")


@bot.command(name="ibrw")
async def ibrw(ctx: commands.Context, *, _unused: str = "") -> None:
    attachment = ctx.message.attachments[0] if ctx.message.attachments else None
    await deobfuscate_attachment(ctx, attachment, "ironbrew1")


@bot.command(name="deobfs", aliases=["deobfuscators", "engines"])
async def deobfs(ctx: commands.Context) -> None:
    await ctx.reply(embed=supported_embed(), mention_author=False)


@bot.command(name="help")
async def help_command(ctx: commands.Context) -> None:
    embed = supported_embed()
    embed.description = (
        "Upload a Lua/Luau source file with `.lph15` or `.ibrw`. "
        "The bot returns the generated `.luau` output as a file."
    )
    await ctx.reply(embed=embed, mention_author=False)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Attach a source file and try again.", mention_author=False)
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
        raise RuntimeError(f"Cannot find the deobfuscator CLI: {DEOB_SCRIPT}")
    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"Bot startup failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        raise
