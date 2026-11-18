#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
DOTNET="$RUNTIME/dotnet"
SDK="$RUNTIME/sdk8"
NUGET="$RUNTIME/nuget"
JAVA="$RUNTIME/java"
NODE="$RUNTIME/node"
TEMP="$RUNTIME/setup-tmp"

IRONVEIL_COMMIT="64b27cfd0cb80919ccefdc8a2e61d6f7d742fb5a"
SEVENTYSEVEN_COMMIT="57042ff5f134f44a162b6b60570b4815b70ef8d2"
JAY_DIR="$ROOT/deobf/jayfuscator"

mkdir -p "$RUNTIME" "$DOTNET" "$SDK" "$NUGET" "$TEMP"
export DOTNET_ROOT="$DOTNET"
export DOTNET_CLI_HOME="$RUNTIME/dotnet-home"
export NUGET_PACKAGES="$NUGET"
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export DOTNET_MULTILEVEL_LOOKUP=0

curl -fsSL https://dot.net/v1/dotnet-install.sh -o "$TEMP/dotnet-install.sh"
bash "$TEMP/dotnet-install.sh" --channel 8.0 --install-dir "$SDK" --no-path
bash "$TEMP/dotnet-install.sh" --channel 8.0 --runtime dotnet --install-dir "$DOTNET" --no-path
bash "$TEMP/dotnet-install.sh" --channel 9.0 --runtime dotnet --install-dir "$DOTNET" --no-path

curl -fsSL "https://codeload.github.com/prostone55/Ironveil-Deobfuscator-V1/tar.gz/$IRONVEIL_COMMIT" -o "$TEMP/ironveil.tar.gz"
mkdir -p "$TEMP/ironveil"
tar -xzf "$TEMP/ironveil.tar.gz" -C "$TEMP/ironveil" --strip-components=1
rm -rf "$RUNTIME/vendor/ironveil"
mkdir -p "$RUNTIME/vendor/ironveil"
cp -a "$TEMP/ironveil/deobfuscator" "$RUNTIME/vendor/ironveil/deobfuscator"
cp -a "$TEMP/ironveil/Samples" "$RUNTIME/vendor/ironveil/Samples"

curl -fsSL "https://codeload.github.com/Bytecoded1337/77fuscatorDeobfuscator/tar.gz/$SEVENTYSEVEN_COMMIT" -o "$TEMP/77fuscator.tar.gz"
mkdir -p "$TEMP/77fuscator"
tar -xzf "$TEMP/77fuscator.tar.gz" -C "$TEMP/77fuscator" --strip-components=1
rm -rf "$RUNTIME/vendor/77fuscator"
mv "$TEMP/77fuscator" "$RUNTIME/vendor/77fuscator"

bash "$ROOT/scripts/materialize_engine_assets.sh"

rm -rf "$JAY_DIR"
mkdir -p "$JAY_DIR"
tar -xzf "$ROOT/deobf/jayfuscator-assets.tar.gz" -C "$JAY_DIR"
test -s "$JAY_DIR/deobf.js"
test -s "$JAY_DIR/utils/decoder.lua"
test -s "$JAY_DIR/utils/lifter.js"
test -s "$JAY_DIR/utils/optimizer.js"
test -s "$JAY_DIR/utils/renamer.js"

export PATH="$SDK:$DOTNET:$PATH"
"$SDK/dotnet" publish "$RUNTIME/vendor/77fuscator/deobfuscator.csproj" -c Release --no-self-contained -o "$RUNTIME/77fuscator"

if [[ ! -x "$NODE/bin/node" ]]; then
    NODE_ARCHIVE="$ROOT/deobf/v151/vendor/node-v20.19.5-linux-x64.tar.gz"
    if [[ ! -s "$NODE_ARCHIVE" ]]; then
        printf 'The bundled Node.js runtime archive is missing.\n' >&2
        exit 1
    fi
    rm -rf "$TEMP/node" "$NODE"
    mkdir -p "$TEMP/node" "$NODE"
    tar -xzf "$NODE_ARCHIVE" -C "$TEMP/node" --strip-components=1
    cp -a "$TEMP/node/." "$NODE/"
    chmod +x "$NODE/bin/node"
fi

"$NODE/bin/node" --check "$JAY_DIR/deobf.js"
for file in "$JAY_DIR/utils"/*.js; do "$NODE/bin/node" --check "$file"; done

if [[ "${FORCE_BUNDLED_JAVA:-0}" == "1" ]] || { ! command -v java >/dev/null 2>&1 && [[ ! -x "$JAVA/bin/java" ]]; }; then
    JAVA_ARCHIVE="$ROOT/deobf/bin/jre17.tar.gz"
    if [[ ! -s "$JAVA_ARCHIVE" ]]; then
        printf 'The bundled Java 17 runtime archive is missing.\n' >&2
        exit 1
    fi
    rm -rf "$TEMP/java" "$JAVA"
    mkdir -p "$TEMP/java" "$JAVA"
    tar -xzf "$JAVA_ARCHIVE" -C "$TEMP/java"
    JAVA_BINARY="$(find "$TEMP/java" \( -type f -o -type l \) -path '*/bin/java' -print -quit)"
    if [[ -z "$JAVA_BINARY" ]]; then
        printf 'The bundled Java runtime does not contain bin/java.\n' >&2
        exit 1
    fi
    JAVA_HOME_FOUND="$(dirname "$(dirname "$JAVA_BINARY")")"
    cp -a "$JAVA_HOME_FOUND/." "$JAVA/"
    chmod +x "$JAVA/bin/java"
fi

"$DOTNET/dotnet" --list-runtimes | grep -q 'Microsoft.NETCore.App 8\.'
"$DOTNET/dotnet" --list-runtimes | grep -q 'Microsoft.NETCore.App 9\.'
"$NODE/bin/node" --version >/dev/null
if [[ -x "$JAVA/bin/java" ]]; then
    "$JAVA/bin/java" -version >/dev/null 2>&1
fi

rm -rf "$TEMP" "$SDK" "$RUNTIME/dotnet-install.sh" "$RUNTIME/dotnet-home"
printf 'MonLua runtime setup completed.\n'
