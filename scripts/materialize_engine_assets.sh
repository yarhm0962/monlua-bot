#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSET_DIR="$ROOT/deobf/engine_assets"
RUNTIME_DIR="$ROOT/.runtime"
ARCHIVE="$RUNTIME_DIR/monlua-engine-assets.zip"
EXPECTED="b4cbfb3b78dcfb7b98ebb002b1a1f15c9ea2ee57adf22222a0f5e78b0bb2ab72"

mkdir -p "$RUNTIME_DIR"
cat "$ASSET_DIR"/part_*.b64 | base64 -d > "$ARCHIVE"
ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
    rm -f "$ARCHIVE"
    printf 'Engine asset checksum mismatch.\n' >&2
    exit 1
fi
unzip -oq "$ARCHIVE" -d "$RUNTIME_DIR/vendor"
rm -f "$ARCHIVE"
