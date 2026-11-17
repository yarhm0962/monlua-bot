#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
APP_DIR="$RUNTIME/vendor/ironbrew2"
REVISION="1cd6541933808aaa5c9dd28bf94a1510fb42b541"
BASE="https://raw.githubusercontent.com/rex-rbx/Open-Source-Obf-and-Dumper/$REVISION/ib2deobf"

mkdir -p "$APP_DIR/runtimes/linux-x64/native"
FILES=(
    KeraLua.dll
    Loretta.CodeAnalysis.dll
    Loretta.CodeAnalysis.Lua.dll
    Loretta.CodeAnalysis.Lua.Experimental.dll
    LuaAnalysis.Common.dll
    LuaAnalysis.Ironbrew2.dll
    LuaAnalysis.Ironbrew2.deps.json
    LuaAnalysis.Ironbrew2.runtimeconfig.json
    NLua.dll
    Tsu.dll
    input.lua
)

for file in "${FILES[@]}"; do
    curl -fsSL "$BASE/$file" -o "$APP_DIR/$file"
done
curl -fsSL "$BASE/runtimes/linux-x64/native/liblua54.so" -o "$APP_DIR/runtimes/linux-x64/native/liblua54.so"

test -s "$APP_DIR/LuaAnalysis.Ironbrew2.dll"
test -s "$APP_DIR/LuaAnalysis.Ironbrew2.deps.json"
test -s "$APP_DIR/LuaAnalysis.Ironbrew2.runtimeconfig.json"
test -s "$APP_DIR/runtimes/linux-x64/native/liblua54.so"
