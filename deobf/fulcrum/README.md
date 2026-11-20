# Fulcrum detection + recovery

MonLua detects Fulcrum-protected scripts (deobf/obfuscators/fulcrum.py) and
recovers them with a full two-stage static engine (deobf/fulcrum-engine/).

Detection: leading Lua header comments ("obfuscated by fulcrum"), the Fulcrum
VM entry-point pattern, O/Q/U/V decoder call sites, and an exact known-sample
digest. It masks strings and comments before evaluating code signatures.

Recovery (deobf/fulcrum-engine/, wired through the plugin's deobfuscate()):

1. Stage 1, unflat.py: un-flattens the Fulcrum VM skeleton back into readable
   Lua (split-segment reassembly, payload integrity checksums, decoy removal,
   ldexp shim kept, loadstring-or-load kept).
2. Stage 2, polish.py: constant folding, variable renaming, syntax healing
   against the bundled Luau compiler (bin/luau-compile), plus the GUI/decoy
   blocks preserved as-is.

Everything is static analysis: no input file is ever executed and no network
access is performed. The engine verifies its own output (luau-compile, 0
syntax errors) before the plugin accepts it, and a failed run leaves no
output file.
