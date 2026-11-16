#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSET_DIR="$ROOT/deobf/engine_assets"
RUNTIME_DIR="$ROOT/.runtime"
ARCHIVE="$RUNTIME_DIR/monlua-ironbrew2-assets.tar.gz"
EXPECTED="9d6bc0d1f02f8ef9bd0e02fcc186ef73c8f01fd49370007b2ae660574932d89c"

mkdir -p "$RUNTIME_DIR/vendor"
if ! compgen -G "$ASSET_DIR/ib2_part_*.b64" >/dev/null; then
    printf 'IronBrew2 runtime asset parts are missing.\n' >&2
    exit 1
fi
cat "$ASSET_DIR"/ib2_part_*.b64 | base64 -d > "$ARCHIVE"
ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
    rm -f "$ARCHIVE"
    printf 'IronBrew2 asset checksum mismatch.\n' >&2
    exit 1
fi
tar -tzf "$ARCHIVE" | grep -q '^ib2deploy/LuaAnalysis.Ironbrew2.dll$'
tar -xzf "$ARCHIVE" -C "$RUNTIME_DIR/vendor"
rm -f "$ARCHIVE"
rm -rf "$RUNTIME_DIR/vendor/ironbrew2"
mv "$RUNTIME_DIR/vendor/ib2deploy" "$RUNTIME_DIR/vendor/ironbrew2"
test -s "$RUNTIME_DIR/vendor/ironbrew2/LuaAnalysis.Ironbrew2.dll"
test -s "$RUNTIME_DIR/vendor/ironbrew2/runtimes/linux-x64/native/liblua54.so"
