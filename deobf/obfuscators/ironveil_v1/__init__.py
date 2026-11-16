import os
import re
import shutil
import subprocess
from pathlib import Path

from obfuscators.base import Obfuscator

DEOBF_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = DEOBF_ROOT.parent
SCRIPT = REPO_ROOT / ".runtime" / "vendor" / "ironveil" / "index.js"
HEADER = re.compile(r"obfuscated\s+using\s+ironveil\s+v?1\b", re.IGNORECASE)


class IronveilV1(Obfuscator):
    name = "ironveil_v1"
    label = "Ironveil v1"

    def detect(self, source, analysis=None):
        if HEADER.search(source[:12000]):
            self.last_evidence = ["Ironveil v1 source banner"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        node = shutil.which("node")
        if not node:
            candidate = REPO_ROOT / ".runtime" / "node" / "bin" / "node"
            if candidate.is_file():
                node = str(candidate)
        if not node:
            raise RuntimeError("Node.js is unavailable. Set NODE_VERSION to 22.23.5 in the Render service environment.")
        if not SCRIPT.is_file():
            raise RuntimeError("Ironveil v1 files are missing. Run scripts/setup_render_runtimes.sh.")
        destination = job.path("_ironveil_result.lua")
        timeout = max(30, min(1800, int(getattr(job.args, "timeout", 90) or 90)))
        try:
            result = subprocess.run(
                [node, str(SCRIPT), str(job.source_path), destination],
                cwd=str(SCRIPT.parent),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Ironveil v1 exceeded its execution time limit.") from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "The engine returned no diagnostic output.").strip()
            raise RuntimeError("Ironveil v1 failed: " + detail[-900:])
        if not os.path.isfile(destination) or os.path.getsize(destination) == 0:
            raise RuntimeError("Ironveil v1 did not produce a readable output file.")
        return destination
