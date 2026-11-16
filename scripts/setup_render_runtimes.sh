#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
DOTNET="$RUNTIME/dotnet"
SDK="$RUNTIME/sdk8"
NUGET="$RUNTIME/nuget"
JAVA="$RUNTIME/java"

mkdir -p "$RUNTIME" "$DOTNET" "$SDK" "$NUGET"
export DOTNET_ROOT="$DOTNET"
export DOTNET_CLI_HOME="$RUNTIME/dotnet-home"
export NUGET_PACKAGES="$NUGET"
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1

curl -fsSL https://dot.net/v1/dotnet-install.sh -o "$RUNTIME/dotnet-install.sh"
bash "$RUNTIME/dotnet-install.sh" --channel 8.0 --install-dir "$SDK" --no-path
bash "$RUNTIME/dotnet-install.sh" --channel 8.0 --runtime dotnet --install-dir "$DOTNET" --no-path
bash "$RUNTIME/dotnet-install.sh" --channel 9.0 --runtime dotnet --install-dir "$DOTNET" --no-path

export PATH="$SDK:$DOTNET:$PATH"
bash "$ROOT/scripts/materialize_engine_assets.sh"

"$SDK/dotnet" publish "$RUNTIME/vendor/77fuscator/deobfuscator.csproj" -c Release --no-self-contained -o "$RUNTIME/77fuscator"
"$SDK/dotnet" restore "$ROOT/deobf/ironbrew2/restore.csproj" --packages "$NUGET"

if ! command -v java >/dev/null 2>&1 && [[ ! -x "$JAVA/bin/java" ]]; then
    mkdir -p "$JAVA"
    tar -xzf "$ROOT/deobf/bin/jre17.tar.gz" -C "$JAVA" --strip-components=1
    if [[ ! -x "$JAVA/bin/java" ]]; then
        JAVA_BINARY="$(find "$JAVA" -type f -path '*/bin/java' -print -quit)"
        if [[ -z "$JAVA_BINARY" ]]; then
            printf 'Bundled Java runtime does not contain a bin/java executable.\n' >&2
            exit 1
        fi
        JAVA_HOME_FOUND="$(dirname "$(dirname "$JAVA_BINARY")")"
        ln -s "$JAVA_HOME_FOUND/bin" "$JAVA/bin"
        if [[ -d "$JAVA_HOME_FOUND/lib" ]]; then
            ln -s "$JAVA_HOME_FOUND/lib" "$JAVA/lib"
        fi
    fi
fi

rm -rf "$SDK" "$RUNTIME/dotnet-install.sh" "$RUNTIME/dotnet-home"
printf 'MonLua runtime setup completed.\n'
