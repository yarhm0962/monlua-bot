# Luraph v15.1 integration

The .lrph15.1 command uses the ServerDeadd/Luraph-v15.1-Deobfuscator source pinned at commit 337d9563202559c092a7a9618c4ac284aceae385.

The Node.js entry point and Python devirtualizer are stored in this directory. The upstream prebuilt Linux Luau binary requires CPU instructions that are not available on every deployment runner, so the CI workflow builds the upstream-patched Luau 0.739 runtime with the portable compiler settings from build_luau.py. The tested luau and luau-ast binaries are committed to deobf/v151/bin so the bot does not need to download or compile them at startup.

Node.js 18 or newer and Python 3.10 or newer are required. The bot uses a compatible system Node.js installation when available and falls back to the existing vendored Node.js 20 runtime. The bot pins the Python executable to the same interpreter used by the service and limits the Luau subprocess virtual memory for the Render memory budget.

The bot runs three deterministic Python hash-seed candidates sequentially, keeping the result with the fewest unrecovered VM blocks and then the most recovered functions. Sequential execution avoids multiplying Python memory use on the small Render instance. The bot requires a zero-unrecovered-block result before delivering output; incomplete lifts are reported as failures instead of being presented as working source.

The CI workflow compiles the Python and JavaScript modules, runs bot regression tests, validates the Luau runtime models, executes the public Luraph v15.1 sample regression suite using the same sequential candidate strategy, and then commits portable runtime binaries when the main-branch build succeeds.

Use this engine only to inspect scripts you own, are authorized to analyze, or are reviewing for safety. The upstream project is MIT licensed; its license is included in LICENSE.
