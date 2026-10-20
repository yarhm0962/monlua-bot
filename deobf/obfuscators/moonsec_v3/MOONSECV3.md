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


## Update 2026-10-20: real Lua output

The deobfuscator now runs the upstream binary's `-dev` mode per candidate (real Lua 5.1 bytecode, `\x1bLuaQ` header) and decompiles it with unluac (Java, vendored JRE 17 + unluac.jar in `../bin/`, extracted to /tmp/monlua-jre at runtime). Result is genuine Lua source, not a bytecode listing. Falls back to `-dis` + beautify when Java or unluac fails. Previously the bot output raw VM bytecode blocks (`function func_XXXX(...)  [Slots: ...]`).
