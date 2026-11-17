import base64
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from obfuscators.base import Obfuscator

DEOBF_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = DEOBF_ROOT.parent
APP_DIR = REPO_ROOT / ".runtime" / "vendor" / "ironbrew2"
APP = APP_DIR / "LuaAnalysis.Ironbrew2.dll"
DOTNET = REPO_ROOT / ".runtime" / "dotnet" / "dotnet"
NATIVE = APP_DIR / "runtimes" / "linux-x64" / "native"
HEADER = re.compile(r"iron\s*brew\s*2", re.IGNORECASE)


def _dotnet():
    if DOTNET.is_file():
        return str(DOTNET)
    return shutil.which("dotnet")


class Ironbrew2(Obfuscator):
    name = "ironbrew2"
    label = "IronBrew2"

    def detect(self, source, analysis=None):
        leading = source[:20000]
        if HEADER.search(leading):
            self.last_evidence = ["IronBrew2 version marker"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        key = (os.getenv("ORACLE") or os.getenv("IRONBREW2_ORACLE_KEY") or "").strip()
        if not key:
            raise RuntimeError("IronBrew2 needs the ORACLE environment variable in the Render service.")
        dotnet = _dotnet()
        required = [APP, APP_DIR / "LuaAnalysis.Ironbrew2.deps.json",
                    APP_DIR / "LuaAnalysis.Ironbrew2.runtimeconfig.json",
                    APP_DIR / "LuaAnalysis.Common.dll", NATIVE / "liblua54.so"]
        missing = [str(path) for path in required if not path.is_file()]
        if not dotnet or missing:
            detail = ", ".join(missing) if missing else ".NET 9 runtime"
            raise RuntimeError("IronBrew2 runtime is incomplete: " + detail + ". Rebuild the Render service.")
        work = Path(job.path("_ironbrew2_work"))
        work.mkdir(parents=True, exist_ok=True)
        bytecode = work / "recovered.luac"
        destination = Path(job.path("_ironbrew2_result.lua"))
        env = os.environ.copy()
        env["DOTNET_ROOT"] = str(REPO_ROOT / ".runtime" / "dotnet")
        env["NUGET_PACKAGES"] = str(REPO_ROOT / ".runtime" / "nuget")
        env["LD_LIBRARY_PATH"] = str(NATIVE) + os.pathsep + env.get("LD_LIBRARY_PATH", "")
        timeout = max(30, min(1800, int(getattr(job.args, "timeout", 90) or 90)))
        try:
            lifted = subprocess.run(
                [dotnet, str(APP), str(job.source_path), str(bytecode)],
                cwd=str(APP_DIR),
                env=env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("IronBrew2 bytecode recovery exceeded its execution time limit.") from exc
        if lifted.returncode != 0 or not bytecode.is_file() or bytecode.stat().st_size == 0:
            detail = (lifted.stderr or lifted.stdout or "The IronBrew2 bytecode lifter returned no diagnostic output.").strip()
            raise RuntimeError("IronBrew2 failed: " + detail[-900:])
        payload = json.dumps(
            {"script": base64.b64encode(bytecode.read_bytes()).decode("ascii"), "decompilerOptions": {}}
        ).encode("utf-8")
        endpoint = "https://oracle.mshq.dev/decompile?" + urllib.parse.urlencode({"key": key, "version": "2"})
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "MonLuaBot/1.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=min(timeout, 180)) as response:
                recovered = response.read().decode("utf-8-sig", errors="replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read(800).decode("utf-8", errors="replace")
            raise RuntimeError("IronBrew2 Oracle rejected the bytecode (HTTP " + str(exc.code) + "). " + detail[:500]) from None
        except Exception as exc:
            raise RuntimeError("IronBrew2 Oracle request failed: " + type(exc).__name__) from None
        try:
            parsed = json.loads(recovered)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            if parsed.get("error"):
                raise RuntimeError("IronBrew2 Oracle error: " + str(parsed["error"])[:700])
            for field in ("text", "output", "code", "result"):
                if isinstance(parsed.get(field), str):
                    recovered = parsed[field]
                    break
        if not recovered.strip():
            raise RuntimeError("IronBrew2 Oracle returned an empty decompilation result.")
        destination.write_text(recovered.rstrip() + "\n", encoding="utf-8")
        return str(destination)
