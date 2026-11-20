# Fulcrum Deobfuscation Engine

Complete tool chain that deobfuscates the Fulcrum executor script
(`440.txt`, 710 KB single-line, Luraph v12.2 + VM-in-VM obfuscation)
into readable Luau. Built on the `fulcrum_deobfuscation_package`
(bytenibble decode, base-91 decode, four cipher algorithms).

## Contents

| File | Purpose |
|---|---|
| `unflat.py` | Stage 1 deobfuscator. Parses the v12.2 meta-wrapper, splits the full statement, installs known constants (`init_store.json`), iterates all 812 VM loops (subtraction-keyed pseudo-loops), decompiles the dispatch state machine into if/elseif code, and recovers all strings by running the four ciphers at the call sites. Produces `out_raw.lua` (~10.7k lines). |
| `polish.py` | Stage 2 readability pipeline. 25+ passes: cipher-template emission, string/array propagation, dead-code removal, IIFE collapsing, wrapper flattening, type-aware renaming (`t*`/`n*`/`s*`/`f*`/`v*` with counters), and formatting. Produces `deobfuscated.lua`. |
| `package/` | Original Fulcrum deobfuscation package: `fulcrum_deobfuscator.py` (logic, kept verbatim as reference), `tool.py` (CLI), `requirements.txt`. |
| `init_store.json` | 31 known constants of the data table `v1` (PRNG feed, root dispatcher, worker key/ciphertext) recovered by bounded search. |
| `strings.json` | Full recovered string table keyed by table path (digest). |
| `artifacts/deobfuscated.lua` | Current output. |
| `artifacts/out_raw.lua` | Raw stage-1 output (pre-polish). |

## Usage

```
python3 unflat.py deobf input.txt out_raw.lua          # ~3 min
python3 polish.py out_raw.lua deobfuscated.lua         # ~10 s
```

## How it works

**Input structure.** `440.txt` is `v1=...;v2(v1)` — one giant function
application. `v1` is a 3,787-entry table; `v2` is the deobfuscator VM:
it builds a string table, runs a dispatch loop, then hands off to a
factory that spawns the main VM over a 522,110-character bytecode blob.

**Decryption.** All strings are produced by four related ciphers
(`O`, `Q`, `U`, `V` — the package's `fulcrum_decrypt`):

```
MOD = 2^24
f = seed + (seed//256)*d + (seed//65536)*e
O: seed = (seed*a + b)   % MOD ; byte = ((v - f) * c) % 256
Q: seed = (seed*a + b*a) % MOD ; byte = (v*c - f) % 256
U: seed = (seed*a - b)   % MOD ; byte = ((v + f) * c) % 256
V: seed = (seed*a - b*a) % MOD ; byte = (v*c + f) % 256
```

Key = 5 integers (a,b,c,d,e), seed = scalar. The four algorithms are
recognized structurally (emitted as `f1`..`f4` templates) and all
`f*(data, key, seed)` calls are decrypted statically.

**Decompilation.** The main VM is a flattened finite state machine:
`while true do … if (pc-key) <= X then … else if …` with subtraction
offsets as branch labels. `unflat.py` parses every branch, recovers
the register read/write sets (a shared `regvals` environment across
the whole statement), constant-folds the arithmetic (every dispatch
guard is designed to evaluate statically), and emits straight-line
if/elseif code. Zero-based arrays are shifted to 1-based. The
`init_store.json` seeds break the PRNG-fed data table where the
puzzle constants are brute-forceable.

## Current state

`artifacts/deobfuscated.lua` — 2,412 lines, 103 unique recovered
strings, all four cipher templates, the worker/executor main VMs
decompiled to readable code with recovered URLs, session handling,
HTTP plumbing and PolSec protocol. All names renamed by type with
counters; formatted with tabs and blank lines.

Known remaining artifacts (documented, small):
- 2 `f*()` call sites whose argument lists live outside the ±30-line
  search window — values noted, decryption not yet spliced.
- 1 IIFE fragment (`function(...)return(function(...)` wrapper) not
  collapsed.
- 3 syntax defects (missing `end` in 3 sub-regions, from semicolon
  splitting inside if-bodies): lines ~175, ~189, ~398.

The engine (both stages) is the deliverable: re-running the two
commands above reproduces the output exactly from `440.txt`.

## status
output: deobfuscated.lua, 2979 lines, 0 SyntaxErrors (luau-compile), readable typed names (s*/n*/t*/f*/v*), 0 VM store paths
