# fulcrum deobfuscation package

Deobfuscates the Fulcrum polsec Luau protector script into fully readable Luau.

## contents
- deobfuscated.lua   -- the deobfuscated output (header: -- deobfuscated by discord.gg/printed)
- engine/unflat.py   -- first stage: decrypts the O/Q/U/V ciphers and unflattens the VM
- engine/polish.py   -- second stage: cleans, flattens VM store cells, readable typed names,
                        format + syntax healing (luau-compile oracle)
- engine/init_store.json, engine/strings.json -- recovered store init + string table
- engine/artifacts/  -- raw stage-1 output (out_raw.lua) + final deobfuscated.lua
- engine/package/    -- the original deobfuscation package scripts (from the dropbox zip)

## usage
  python3 engine/unflat.py deobf <input.txt> out_raw.lua     (~3 min)
  python3 engine/polish.py out_raw.lua deobfuscated.lua       (~10 s)

verify with luau-compile --binary deobfuscated.lua (no output path): success = 0 SyntaxErrors.

## output style
reference luraph-style: typed counters (s*, n*, t*, f*, v*), real strings inline,
cipher templates named f1..f4 (O/Q/U/V, `local a,b,c,d,e = key[1]..key[5]`),
no VM store cells, no obfuscated identifiers, Luau compound ops where applicable.
