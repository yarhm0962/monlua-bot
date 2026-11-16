# Luraph v15.1 integration

The .lrph15.1 command uses the pinned ServerDeadd/Luraph-v15.1-Deobfuscator source at commit 337d9563202559c092a7a9618c4ac284aceae385.

The Node.js entry point and Python devirtualizer are stored in this directory. The Luau runtime binaries are downloaded from that exact upstream commit when the bot starts, then verified against their Git blob SHA-1 and expected byte sizes before they are installed. This keeps the deployment binary in sync with the source revision without checking large platform-specific executables into the repository.

Node.js 18 or newer and Python 3.10 or newer are required. The bot uses its system Node.js installation when available and falls back to the existing vendored Node.js 20 runtime. The bot pins the Python executable to the same interpreter used by the service and limits the Luau subprocess virtual memory for the Render memory budget.

The CI workflow installs and verifies the pinned runtime, checks JavaScript and Python syntax, runs the datatype and Luau lowering checks, and executes the upstream public sample regression suite.

Use this engine only to inspect scripts you own, are authorized to analyze, or are reviewing for safety. The upstream project is MIT licensed; its license is included in LICENSE.
