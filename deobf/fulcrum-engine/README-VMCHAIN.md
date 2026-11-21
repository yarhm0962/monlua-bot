# Fulcrum Deobfuscator (VM-interpreter build support)

Pipeline for Fulcrum (polsec.net) builds whose recovered payload is a flattened
VM interpreter:

1. `fulcrum.py deobf <in> <out>` auto-detects the VM-interpreter build
   (decode anchor `local u=I(F,h);local L=u//32;...`) and runs `vmfinal.py`.
2. `vmfinal.py` builds the dispatch tree (vmtree), walks the reachable (L,u)
   states from the entry constants (vmwalk), and rewrites the multi-hundred-KB
   flattened interpreter body into a compact dispatch chain keyed on the
   reachable states. The second-layer dispatch and the iteration gate are kept
   verbatim.
3. Output is verified with the bundled Luau compiler (`bin/luau-compile`).

Verification done on the recovered PolSec remote-loader payload
(549,254 bytes): the walk produced 54 reachable states (54 handlers emitted),
the deobfuscated file is 26,052 bytes (down from 549,254), compiles clean, and
an instrumented run of both files under stubbed Roblox globals produced the
identical 43-state dispatch trace, ending at the same halt state (3272691,0)
where the interpreter spins by design.

Commands:
  deobf <in> <out>    auto-detect + full deobfuscation (VM build or two-stage)
  vmchain <in> <out>  VM-interpreter build only
  stage1/polish/...   the original two-stage pipeline (unchanged)
