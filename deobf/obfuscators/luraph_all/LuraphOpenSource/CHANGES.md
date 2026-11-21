# Luraph v15.1 engine swap

The `luraph_v15` engine (`core/obfuscators/luraph_v15/devirt.py` and `vmmap.py`) was replaced with the one from the
"Luraph v15.1 Deobfuscator" package. The previous engine failed on real v15.1 scripts: closure creation came out as
`error("devirt: value <...OpenUps object...> in an expression")` and a 1.5 MB sample devirtualized to ~14 KB with
unresolved blocks. With the new engine the five bundled v15.1 samples devirtualize cleanly (e.g. 665 functions,
0 unlifted blocks, 0 unstructured jumps, ~703 KB of readable Luau).

Everything else (v14.7/14.8/14.9/v14 engines, header detection, fault tolerance, `driver.py`, sl_post, lift_guard,
SigmaBot integration) is unchanged. Detection of "Luraph 15.0 / 15.1" still routes to `luraph_v15`.

# LuraphOpenSource — robustness update

## Root causes fixed
1. **`luau-ast` not found by the v14.7 / 14.8 / 14.9 lifter** (`core/obfuscators/luraph_v14_{7,8,9}/vmmap.py`).
   It looked in `core/bin/` (never exists) instead of `LuraphOpenSource/bin/`, so every lift died with
   `FileNotFoundError` and the run fell back to the behaviour trace. Now uses the shared locator
   (`harness.run_luau_ast`: `bin/`, then `PATH`) like the v14/v15 engines.
2. **Header detection too strict** (`src/detect.js`). The Luraph header had to be in the first 500 chars with exact
   case/spacing; a key line, BOM or pasted prefix made the file "unknown" -> trace-only. Now: header searched in the
   first 8 KB, case/spacing tolerant, `v14.10+` handled, plus structural detection for headerless v14/v15, and an
   AST probe (`deob.js`) as the last resort before giving up.
3. **`core/sl_post.py` could not even be imported** (two corrupted regex literals). Fixed. It is now opt-in
   (`DEOB_SL_POST=1`) because it strips every comment (including the engine's own warnings) and adds third-party
   watermark/advert lines; it never ran in production before, so default behaviour is unchanged.
4. **`sys.exit()` inside the v14/v15 lift** escaped every handler and killed the run (no fallback output).
   Replaced by guarded lifts.

## Fault tolerance added
- Lift retries once with relaxed walk limits (`core/lift_guard.py`) before giving up.
- Strict v14.x engine -> lenient v14 engine on the same trace (no re-trace) when the first is empty/broken/partial.
- A later constant round failing no longer discards an earlier good lift; a failing request-walk goes straight to a full lift.
- Trace run timing out -> one retry with a shorter script budget.
- VM instrumentation failure (AST parse) -> trace-only instead of aborting the file.
- Guessed family wrong -> the other family (v14 <-> v15) is tried (`--no-engine-fallback` disables).
- Partial lifts are kept and labelled (`unresolved` markers counted) instead of being thrown away.
- BOM removed before parsing.
- Fallback traces now start with an explicit "NOT the original source" note and a reason.
  `deob.js` prints `[result] kind=devirt|trace|loadstring-payload` on stderr.

## Self-test
`node selftest.js`

# Devirtualization-failure hardening (v14.7 / v14.8 / v14.9 / v15 / v14 engines)

Goal: a single misread instruction or function must no longer cost the whole script its devirtualization
(the cause of "huge output, but parts still unreadable" and of silent drops to the behaviour trace).

1. **Per-instruction containment** (`core/obfuscators/*/devirt.py`, walk loop). The symbolic stepper only caught
   `Unsupported`; any other exception from an opcode handler (KeyError, IndexError, TypeError, ...) aborted the
   walk of the whole function. It now marks just that VM state as unlifted ("internal lifter error at mode:pc")
   and keeps walking.
2. **Per-closure containment** (v14.7/14.8/14.9 `FunctionLifter.closure`). v15 already stubbed a nested
   function that failed to lift; the v14.x engines only handled `Unsupported`, so any other error in one nested
   function killed the entire lift. They now stub that one function and keep everything else.
3. **Request/frame walks** (`_walk_one`, `frame_regs`) no longer abort on a non-`Unsupported` error.
4. **Readability passes isolated** (`core/backend.py`). If one of the idiom/variable passes raises, the function keeps
   its structured (but untidied) body instead of failing; previously that lost the function (or the script).
5. **Tests**: `tests/lowering_selftest.py` (run by `node selftest.js`): random CFGs lower with no exception and
   no `unstructured jump` stub, and an injected pass failure is contained.

Known limit: a function that mixes recognised `for` loops with a control-flow shape the structurer cannot
express still ends in `error("devirt: unstructured jump ...")` (the state-machine fallback cannot split a `for`).
Output of healthy inputs is byte-identical to before.
