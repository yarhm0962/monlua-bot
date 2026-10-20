# MoonSec V3 (moonsec_v3)

Header: `--[[This file was protected with MoonSec V3 ...]]):gsub('.+', ...)`.

Engine: bin/MoonsecDeobfuscator (C#, self-contained linux-x64, built from
tupsutumppu/MoonsecDeobfuscator) plus bin/liblua54.so next to it (NLua's
runtime; the binary loads it from its own folder). The tool runs with
DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1 so no ICU is needed on Render.

What it does: parses the obfuscated script, decodes the MoonSec constant
strings, rewrites the VM loader and emits Lua 5.1 bytecode. Output here is
the bytecode as a readable disassembly (-dis mode); the raw bytecode
(-dev) is binary and useless in Discord. There is no decompiler in the
tool, so source recovery stops at the disassembly.

Failure mode: a non-MoonSec input throws a .NET exception; the plugin
surfaces the first Exception line as a clean error.
