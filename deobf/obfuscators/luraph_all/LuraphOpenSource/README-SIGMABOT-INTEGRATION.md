# SigmaBot Luraph (All Versions) integration

This bundle contains the updated bot and the open-source Luraph devirtualizer export supplied in the conversation.

## Supported Luraph versions

The `/deobfuscate` command and configured deobfuscation prefix now expose one option:
`Luraph (All Versions)`.

The attached engine is routed by detected version:
- Luraph 14.7 -> `luraph_v14_7`
- Luraph 14.8 -> `luraph_v14_8`
- Luraph 14.9 -> `luraph_v14_9`
- Luraph 15.0 -> `luraph_v15`
- Luraph 15.1 -> `luraph_v15`

The `.help` supported-obfuscators page uses the same unified label.

## Runtime requirements

Install/provide:
- Node.js 18 or newer
- Python 3.10 or newer
- The Luau CLI runtime and `luau-ast` executable built for your host

Place the Luau executables here:
- `LuraphOpenSource/bin/luau` (Windows: `luau.exe`)
- `LuraphOpenSource/bin/luau-ast` (Windows: `luau-ast.exe`)

The follow-up export supplied `build_luau.py` and `protocol.json`. It still does not include prebuilt Luau binaries. You can build them from the supplied script (requires Git, CMake, and a C++ compiler), or provide compatible binaries. The engine can also find those executables on `PATH`.

Keep `LuraphOpenSource/` in the same directory as the bot file. Alternatively, set:
- `LURAPH_OPEN_SOURCE_ROOT` to the absolute path of the extracted `LuraphOpenSource` directory
- `LURAPH_NODE` if Node.js is installed under a nonstandard executable name/path

The bot runs the devirtualizer in a separate process with a timeout. The supplied source engine is used locally; the old Luraph API route is no longer used for this unified option.

## Files

- `bot.py` — updated SigmaBot source
- `LuraphOpenSource/` — supplied open-source engine source and runtime data

## Remaining setup requirement

The supplied follow-up archive has now been integrated: `protocol.json` is at the project root and `build_luau.py` is included. The Luau executables are still absent. Build them on the deployment host with:

```bash
cd LuraphOpenSource
python build_luau.py --portable
```

This build requires Git, CMake, and a working C/C++ toolchain. It fetches the configured Luau source release and writes `bin/luau` and `bin/luau-ast` (Windows executables use `.exe`). Alternatively, provide compatible prebuilt executables in `LuraphOpenSource/bin/`.

The CLI's `--detect` path was smoke-tested after adding `protocol.json`. Full deobfuscation has not yet been verified because the Luau executables are not present in this environment.
