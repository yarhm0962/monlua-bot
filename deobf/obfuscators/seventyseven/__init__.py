import os
import re
import shutil
import subprocess
from pathlib import Path

from obfuscators.base import Obfuscator

DEOBF_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = DEOBF_ROOT.parent
APP = REPO_ROOT / ".runtime" / "77fuscator" / "deobfuscator.dll"
DOTNET = REPO_ROOT / ".runtime" / "dotnet" / "dotnet"
UNLUAC = DEOBF_ROOT / "bin" / "unluac.jar"
HEADER = re.compile(r"77fuscator\s+0\.6\.1\s+early\s+build", re.IGNORECASE)


def _dotnet():
    if DOTNET.is_file():
        return str(DOTNET)
    return shutil.which("dotnet")


def _java():
    bundled = REPO_ROOT / ".runtime" / "java" / "bin" / "java"
    if bundled.is_file():
        return str(bundled)
    return shutil.which("java")


class SeventySevenFuscator(Obfuscator):
    name = "77fuscator"
    label = "77fuscator"

    def detect(self, source, analysis=None):
        if HEADER.search(source[:30000]):
            self.last_evidence = ["77fuscator 0.6.1 build watermark"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        dotnet = _dotnet()
        java = _java()
        if not dotnet:
            raise RuntimeError(".NET 8 runtime is unavailable. Run scripts/setup_render_runtimes.sh.")
        if not APP.is_file():
            raise RuntimeError("77fuscator has not been built. Run scripts/setup_render_runtimes.sh.")
        if not java or not UNLUAC.is_file():
            raise RuntimeError("The Java runtime or unluac.jar is unavailable.")
        work = Path(job.path("_77fuscator_work"))
        work.mkdir(parents=True, exist_ok=True)
        bytecode = str(work / "recovered.luac")
        destination = job.path("_77fuscator_result.lua")
        env = os.environ.copy()
        env["DOTNET_ROOT"] = str(REPO_ROOT / ".runtime" / "dotnet")
        env["NUGET_PACKAGES"] = str(REPO_ROOT / ".runtime" / "nuget")
        timeout = max(30, min(1800, int(getattr(job.args, "timeout", 90) or 90)))
        try:
            lifted = subprocess.run(
                [dotnet, str(APP), str(job.source_path), "-o", bytecode, "--strings"],
                cwd=str(APP.parent),
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("77fuscator exceeded its execution time limit.") from exc
        if lifted.returncode != 0 or not os.path.isfile(bytecode) or os.path.getsize(bytecode) == 0:
            detail = (lifted.stderr or lifted.stdout or "The bytecode lifter returned no diagnostic output.").strip()
            raise RuntimeError("77fuscator failed: " + detail[-900:])
        try:
            decompiled = subprocess.run(
                [java, "-jar", str(UNLUAC), bytecode],
                cwd=str(work),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("The Lua 5.1 bytecode-to-source pass exceeded its execution time limit.") from exc
        if decompiled.returncode != 0 or not decompiled.stdout.strip():
            detail = (decompiled.stderr or decompiled.stdout or "unluac returned no source.").strip()
            raise RuntimeError("77fuscator output could not be converted to Lua source: " + detail[-900:])
        Path(destination).write_text(decompiled.stdout.rstrip() + "\n", encoding="utf-8")
        return destination
