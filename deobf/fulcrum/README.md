# Fulcrum detection

MonLua includes a code-aware Fulcrum detector and a reference digest for the exact sample described in the supplied archive.

Recovery is intentionally disabled. The archive's full engine imports missing `tool.py` and `lualex.py` modules using absolute paths from another machine. Its fallback package explicitly describes itself as an experimental partial decoder that does not perform full VM devirtualization. The archive does not contain the original reference input, so the full engine cannot be validated end-to-end.

The detector uses leading Lua header comments, the Fulcrum VM entry-point pattern, O/Q/U/V decoder call sites, and an exact known-sample digest. It masks strings and comments before evaluating executable-code signatures. Regression tests check the existing Centurion and Luraph v15.1 sample corpora.

The engine appears as detection-only in the MonLua picker until a complete, self-contained, authorized recovery implementation and its original test inputs are available.
