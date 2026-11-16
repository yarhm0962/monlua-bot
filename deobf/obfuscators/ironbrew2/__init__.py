import base64
import json
import os
import re
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
HEADER = re.compile(r"ironbrew\s*2", re.IGNORECASE)


class Ironbrew2(Obfuscator):
    name = "ironbrew2"
    label = "IronBrew2"

    def detect(self, source, analysis=None):
        leading = source[:16000]
        if HEADER.search(leading):
            self.last_evidence = ["IronBrew2 version marker"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        key = (os.getenv("ORACLE") or os.getenv("IRONBREW2_ORACLE_KEY") or "").strip()
        if not key:
            raise RuntimeError("The ORACLE environment variable is not configured in Render.")
        if not DOTNET.is_file() or not APP.is_file():
            raise RuntimeError("The IronBrew2 .NET 9 runtime or engine files are missing.")
        work = Path(job.path("_ironbrew2_work"))
        work.mkdir(parents=True, exist_ok=True)
        bytecode = work / "recovered.luac"
        destination = job.path("_ironbrew2_result.lua")
        env = os.environ.copy()
        env["DOTNET_ROOT"] = str(REPO_ROOT / ".runtime" / "dotnet")
        env["NUGET_PACKAGES"] = str(REPO_ROOT / ".runtime" / "nuget")
        timeout = max(30, min(1800, int(getattr(job.args, "timeout", 90) or 90)))
        try:
            lifted = subprocess.run(
                [str(DOTNET), str(APP), str(job.source_path), str(bytecode)],
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
            detail = (lifted.stderr or lifted.stdout or "The IronBrew2 lifter returned no diagnostic output.").strip()
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
            raise RuntimeError("Oracle decompilation failed with HTTP " + str(exc.code) + (": " + detail if detail else "")) from None
        except Exception as exc:
            raise RuntimeError("Oracle decompilation request failed: " + type(exc).__name__) from None
        try:
            parsed = json.loads(recovered)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            if parsed.get("error"):
                raise RuntimeError("Oracle rejected this bytecode: " + str(parsed["error"])[:700])
            for field in ("text", "output", "code", "result"):
                if isinstance(parsed.get(field), str):
                    recovered = parsed[field]
                    break
        if not recovered.strip():
            raise RuntimeError("Oracle returned an empty decompilation result.")
        destination_path = Path(destination)
        destination_path.write_text(recovered.rstrip() + "\n", encoding="utf-8")
        return str(destination_path)
