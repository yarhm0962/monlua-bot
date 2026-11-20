# Fulcrum / Luraph reverse-engineering toolkit

This is the complete set of engine source and capture components currently available in this workspace, not a finished universal Fulcrum deobfuscator. The `fulcrum` directory contains case-specific analyses and capture helpers; it does **not** contain an automated full Fulcrum control-flow devirtualizer. The `deobf` directory contains the dynamic deobfuscator and experimental Luraph v15 symbolic lifter, including fixes made for the supplied payload. Fulcrum and Luraph are different obfuscators; support for one does not imply support for the other.

## Layout

- `deobf/`: deobfuscator source, plugins, Luau harness, and Linux x86-64 Luau and AST binaries. See `deobf/deob.py --help` and `deobf/CLAUDE.md` for usage.
- `fulcrum/`: case-specific Lua components and executor capture tools. They are research components, not an integrated standalone engine; several require an executor environment.
- `FULCRUM_ANALYSIS.md`: analysis of the specific loader, not a universal specification.
- `experiments/`: selected symbolic path and child-lifting experiments and a path isolation test. Several experiments depend on captured protos, snapshots, and a case-specific workspace that are not in this engine package. They are included as source for continued work, not as turnkey programs.

## Quick start (Linux x86-64, Python 3)

After extracting, run:

```sh
chmod +x deobf/bin/luau deobf/bin/luau-ast
python3 deobf/deob.py /path/to/input.lua --detect
python3 deobf/deob.py /path/to/input.lua --output /path/to/output.lua
PYTHONPATH=deobf:experiments python3 experiments/test_path_sensitive_step.py
```

The included executables are Linux builds; on other platforms build or supply suitable Luau and luau-ast executables, see `deobf/build_luau.py`. Dynamic tracing is environment-dependent and incomplete; do not treat emitted behavior traces as recovered source. The toolkit does not currently recover the full provided PolSec payload or remove its authentication reliably. A successful command or synthetic test is not proof of functional equivalence. Only run samples you trust in a suitably isolated environment.

The capture component `polsec_dumper.lua` has a blank HWID rather than the user's original identifier; populate it locally if needed. Authentication keys and runtime captures are not distributed in this package.
