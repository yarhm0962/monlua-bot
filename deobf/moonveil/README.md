# MoonVeil v1.4.5 deobfuscator

This public bundle targets MoonVeil Obfuscator v1.4.5 only. It recognizes complete v1.4.5 inputs, recovers serialized prototype graphs where present, infers randomized VM layouts, reconstructs runnable Luau, and validates generated output with the bundled official Luau tools.

The output is behavior-oriented. Obfuscation discards original local names, formatting, and comments, so those cannot be reproduced exactly. Serialized programs are reconstructed into ordinary Luau conditionals, native numeric and generic loops, natural `while` loops, direct calls, vararg forwarding, lexical closures, table literals, folded expressions, named parameters, and conservative semantic names. The reconstruction rules are derived from control-flow and data-flow shapes; they contain no sample names, private opcode numbers, game-specific strings, or per-file source templates.

## Fastest use

From this folder:

```powershell
python -m moonveil decompile "C:\path\obfuscated.lua" `
  -o "C:\path\recovered.luau" `
  --artifacts "C:\path\moonveil-artifacts"
```

Or launch the file-picker interface:

```powershell
python -m moonveil.gui
```

The included launchers provide the same workflows:

- `Decompile File.bat`
- `Start GUI.bat`
- `Verify Installation.bat`

## Requirements

- Python 3.10 or newer
- Official Luau runtime and compiler

The tested Windows binaries are included under `.tools\luau-0.722`. A different runtime can be selected with `--luau`, `LUAU_PATH`, or `PATH`.

## Supported v1.4.5 input families

The structural pipeline currently covers these complete-input families:

- Serialized VM wrappers with randomized identifiers, numeric fields, and opcode assignments
- Indirect serialized wrappers whose constructor alias is selected through flattened control flow
- Source-level transformed programs that use MoonVeil string encoders and arithmetic rewriting without a serialized prototype graph

For serialized programs, the decompiler discovers prototype metadata and VM runtime fields from structure rather than requiring fixed names. It probes lazy instructions with isolated proxy, symbolic, numeric, numeric-zero, table-observation, false, and nil register modes, lifts observed semantics into a canonical IR, and emits runnable Luau.

Common one-prototype downloader programs are cleaned into an explicit form equivalent to:

```lua
local sourceUrl = "https://example.invalid/script"
local downloadedSource = game:HttpGet(sourceUrl)
local loadedChunk = loadstring(downloadedSource)
loadedChunk()
```

General serialized programs use the structured reconstruction backend. The largest fresh regression input reconstructs all 160 prototypes and 17,845 instruction slots without a program-counter dispatcher, then passes compiler and sandbox trace validation.

Release 0.11 extends the high-level reconstruction stage with group-wide return, capture, quiet-upvalue, and `SETLIST` inference; a dedicated zero probe for numeric-zero branches; exact table-slot observation for randomized list operands; and exitless conditional-loop reconstruction. It retains the readability stage introduced in 0.10: iterator emulators become native `for` loops, numeric ranges and natural loop conditions are recognized, one-use register expressions and table construction are folded, terminating branches become guard clauses, loop values and parameters receive conservative names, and one-use closure factories are inlined with scoped capture cells. Shared closure factories remain explicit when inlining would duplicate code.

Source-level transformed inputs first decode provable strings and fold deterministic state. Recognized semantic layouts are then lifted into short, named Luau programs; unrecognized layouts retain runtime-dependent branches in a conservative static fallback.

## Readability profiles

`structured` means every recovered prototype was converted to ordinary Luau control flow and the output contains no register-VM program-counter dispatcher. A `structured-with-fallback-X-of-Y` profile is now reserved for an unseen control-flow form that cannot yet be proven reducible; none of the supplied serialized v1.4.5 regression samples require it.

Recovered names such as `players`, `localPlayer`, `camera`, parameter roles, loop values, and service names are assigned only when dataflow proves their meaning. One-use closures are placed back at their lexical creation sites. Remaining `R<number>`, `captured_*`, and shared-factory `upvalues[...]` names are values whose author-selected names were erased by obfuscation and cannot be recovered exactly.

## Complete files are required

The decompiler cannot recover data that is missing from the input file. It parses every v1.4.5 source before instrumentation. If the source ends inside a string, call, conditional, or function, the command stops with a targeted message:

```text
input is truncated or incomplete MoonVeil v1.4.5 Luau; the parser reached an unfinished source construct. Obtain the complete obfuscated file.
```

This is distinct from an unsupported complete wrapper. Re-download or re-export a truncated file; fragments from separately randomized builds cannot be concatenated safely.

## What `decompile` does

1. Confirms the v1.4.5 banner and parses the complete input without executing it.
2. Selects the serialized, indirect-wrapper, or source-level profile.
3. Runs only the necessary decoding bootstrap inside the API-limited Luau CLI.
4. Captures the prototype graph before protected code receives real external APIs.
5. Infers randomized prototype fields, instruction fields, executor variables, and opcode location.
6. Probes every instruction slot in isolated semantic modes, including numeric-zero branch and post-`SETLIST` table-slot observations.
7. Lifts the observations into canonical semantic IR.
8. Reconstructs conditionals, native generic and numeric loops, natural loops, open calls, varargs, lexical closures, table literals, and returns into ordinary Luau, then applies conservative names, guard clauses, and dataflow-safe expression folding.
9. Compiles the output and, where supported, compares original and recovered proxy traces.

The pipeline fails closed on an unrecognized wrapper, ambiguous field, or semantic operation. It does not invent replacements for unknown instructions.

## Output and artifacts

The path passed to `-o` receives runnable recovered Luau. With `--artifacts`, applicable profiles also write:

- `prototype_graph.json`: lossless typed table graph
- `prototypes.json`: normalized prototype metadata
- `semantic_ir.json`: canonical lifted operations
- `decoded_proxy.json`, `decoded_symbolic_true.json`, `decoded_numeric.json`, `decoded_zero.json`, `decoded_table.json`, `decoded_false.json`, and `decoded_nil.json`: mode-specific observations
- `decode_*_protocol.txt`: raw binary-safe probe protocols
- `decompile_manifest.json`: input hash, selected profile, counts, layout, notes, and validation result

A source-level input has no prototype graph, so its artifact set is smaller.

## Other commands

```powershell
python -m moonveil analyze script.lua --json
python -m moonveil dump script.lua -o output
python -m moonveil extract script.lua -o output\outer_payload.bin
python -m moonveil instrument script.lua -o output\instrumented.luau
python -m moonveil import-protocol captured.txt -o output
```

`extract` and `instrument` are low-level commands for wrappers with a directly embedded payload and standard constructor boundary. Use `decompile` for automatic family selection.

## Verification and limits

Generated Luau is compiled whenever `luau-compile` is available. Serialized wrappers with the standard runtime layout are also run against a proxy-only environment on both sides; observable calls, property access, table writes, and arguments must match in order. Use `--no-verify` only to skip this comparison deliberately.

Direct and indirect serialized wrappers are compiler-validated and compared end to end in the same proxy-only sandbox. If the protected original itself does not terminate within the dedicated 10-second verification budget, decompilation still completes and marks the sandbox comparison as inconclusive; this is distinct from a trace mismatch. Decode and compiler stages retain the full command timeout. Recognized source-level layouts emit compiler-validated semantic reconstructions; unknown layouts use the explicitly marked static fallback. Roblox services, network access, filesystem access, and a working `loadstring` are not granted to the verification sandbox.

The former Golf Yard shortcut is no longer selected automatically. That file now uses the same generic, compiler-checked, trace-verified path as other serialized v1.4.5 programs.

## Supplied corpus results

Release 0.11.0 was validated against the supplied serialized MoonVeil v1.4.5 files and the later real-world sample set. Every listed prototype is reconstructed without `pc ==`, `local registers = {}`, or a VM dispatch loop. The new source cleanup reduced the largest saved output from 37,437 to 24,544 lines while retaining its exact 757-event sandbox trace.

| Input | Recovery result | Validation |
| --- | --- | --- |
| `sample1.lua` | 12/12 prototypes structured, 2,164 instructions | Exact 212-event trace |
| `sample2.lua` | 12/12 prototypes structured, 2,162 instructions | Exact 212-event trace |
| `sample6.lua` | 144/144 prototypes structured, 13,105 instructions | Exact 2,728-event trace |
| `sample8.lua` | 34/34 prototypes structured, 1,746 instructions | Exact 18-event trace |
| `sample9.lua` | 34/34 prototypes structured, 1,779 instructions | Exact 18-event trace |
| `sample10.lua`, `sample11.lua` | 62/62 prototypes structured, 4,104 instructions | Exact 14-event trace per file |
| `sample12.lua` | 5/5 prototypes structured, 409 instructions | Exact 52-event trace |
| `sample13.lua` | 33/33 prototypes structured, 2,008 instructions | Compiles; protected original exceeds verifier timeout |
| `sample14.lua` | 4/4 prototypes structured, 277 instructions | Exact 19-event trace |
| `sample15.lua` | 46/46 prototypes structured, 3,250 instructions | Exact 415-event trace |
| `sample16.lua` | 160/160 prototypes structured, 17,845 instructions | Exact 757-event trace |
| `sample18.lua` | Byte-identical to `sample15.lua`; 46/46 prototypes structured | Exact 415-event trace via identical input |
| `sample20.lua` | Named 11-line remote-loader reconstruction | Exact 7-event trace |
| `sample21.lua` | Byte-identical to `sample6.lua`; 144/144 prototypes structured | Exact 2,728-event trace via identical input |
| `sample22.lua` | 14/14 prototypes structured, 1,101 instructions | Exact 231-event trace |
| `sample23.lua` | 44/44 prototypes structured, 1,912 instructions | Exact 407-event trace |
| `sample24.lua` | 60/60 prototypes structured, 3,018 instructions | Exact 843-event trace |
| `sample25.lua` | 48/48 prototypes structured, 2,318 instructions | Exact 7-event trace |
| `sample26.lua` | 35/35 prototypes structured, 1,836 instructions | Exact 27-event trace |
| `sample27.lua` | 14/14 prototypes structured, 1,034 instructions | Exact 436-event trace |
| `sample28.lua` | 21/21 prototypes structured, 1,813 instructions | Exact 288-event trace |
| `sample29.lua` | 44/44 prototypes structured, 2,331 instructions | Compiles; protected original intentionally does not terminate |

The same structural rules handle each file: randomized opcode identities are inferred per input, `GETVARARGS` is distinguished from close-upvalue operations through its consumers, capture and upvalue operands are validated against prototype bounds, list operands are recovered from observed table slots across the opcode group, and loops are recovered from CFG dominance, strongly connected components, and backedges. An exact trace means the protected and reconstructed programs produced the same ordered observable behavior in the API-limited sandbox. It does not imply restoration of erased comments or author-selected local names.
## Safety

The recovery harness limits external APIs, but arbitrary unprotected statements could exist outside the serialized payload. Use a disposable environment for unknown inputs.

## Tests

```powershell
python -B -m unittest discover -s tests -v
```

Corpus-dependent tests skip when their referenced Downloads files are unavailable. Set `MOONVEIL_V145_CORPUS` to point them at another directory containing the named fixtures.