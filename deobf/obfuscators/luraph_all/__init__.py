"""Luraph (All Versions): unified detection and the vendored Node/Python devirtualizer.

Routes every Luraph build to the vendored LuraphOpenSource engine (deob.js),
which picks the right version family (v14.7, v14.8, v14.9, v15) and
devirtualizes through a Luau runtime trace. Version-specific engines already
registered here (v14.3, v15.0, v15.1) keep priority: this engine scores below
them on their exact versions and is the catch-all for the rest.
"""
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from obfuscators.luraph_v15 import HEADER, HEADER_ANY

_PKG_DIR = Path(__file__).resolve().parent
ROOT = _PKG_DIR / "LuraphOpenSource"
SCRIPT = ROOT / "deob.js"
_REPO_ROOT = _PKG_DIR.parents[2]
_NODE_ARCHIVE = _REPO_ROOT / "deobf" / "v151" / "vendor" / "node-v20.19.5-linux-x64.tar.gz"
_NODE_DIRNAME = "node-v20.19.5-linux-x64"

_V14_PLUGINS = {7: "luraph_v14_7", 8: "luraph_v14_8", 9: "luraph_v14_9"}
_V14_SHAPE_RE = re.compile(
    r"(?:return\s*\(\s*function\s*\(\s*\.\.\.\s*\)"
    r"|local\s+init\s*=\s*\(\s*function\s*\(\s*\.\.\.\s*\)"
    r"|return\s*\(\s*\{)"
)


def header_version(source, analysis=None):
    """(major, minor:int|None) from an official or rebranded Luraph header, else None."""
    from obfuscators.extra_families import LuaAnalysis

    analysis = analysis or LuaAnalysis(source)
    comments = analysis.header[:4000]
    match = HEADER.search(comments)
    if match:
        return match.group(1), int(match.group(2)) if match.group(2) else None
    if HEADER_ANY.search(comments):
        vm = re.search(r"v?(1[3-6])\.(\d+)", comments, re.I)
        if vm:
            return vm.group(1), int(vm.group(2))
        return "unknown", None
    return None


class LuraphAll:
    name = "luraph_all"
    label = "Luraph (All Versions)"
    doc = "LURAPH.md"

    def detect(self, source, analysis=None):
        from obfuscators.extra_families import LuaAnalysis

        analysis = analysis or LuaAnalysis(source)
        version = header_version(source, analysis)
        if version:
            major, minor = version
            if major == "14" and minor is not None:
                if minor in (7, 8, 9):
                    self.last_evidence = [
                        "Luraph v14.%d header; the all-versions engine handles it natively" % minor
                    ]
                    return 1.0
                if minor >= 10:
                    self.last_evidence = [
                        "Luraph v14.%d header; the newest vendored v14 engine is the best match" % minor
                    ]
                    return 0.95
                self.last_evidence = [
                    "Luraph v14.%d header; the version-specific v14.3 engine is the better match" % minor
                ]
                return 0.6
            if major == "15" and minor is not None:
                self.last_evidence = [
                    "Luraph v15.%d header; the version-specific v15 engine is the better match" % minor
                ]
                return 0.7
            if major == "unknown":
                self.last_evidence = ["Luraph header found, but its version is not stated"]
                return 0.55
            self.last_evidence = [
                "Luraph v%s%s header; routed through the vendored v15 engine as the closest match"
                % (major, ("." + str(minor)) if minor is not None else "")
            ]
            return 0.7

        head = analysis.structure[:262144]
        if _V14_SHAPE_RE.search(head) and ("bit32." in head or "LPH" in head):
            self.last_evidence = ["headerless Luraph v14 VM wrapper shape"]
            return 0.7
        self.last_evidence = []
        return 0.0

    def add_arguments(self, ap):
        return

    def _node(self):
        env = os.environ.get("LURAPH_NODE") or os.environ.get("NODE_BIN")
        if env and os.path.isfile(env):
            return env
        found = shutil.which("node")
        if found:
            return found
        target = Path(tempfile.gettempdir()) / "monlua-node"
        exe = target / _NODE_DIRNAME / "bin" / "node"
        if not exe.is_file():
            if not _NODE_ARCHIVE.is_file():
                raise RuntimeError(
                    "node is not installed and the vendored node runtime archive is missing"
                )
            target.mkdir(parents=True, exist_ok=True)
            try:
                with tarfile.open(_NODE_ARCHIVE, "r:gz") as archive:
                    archive.extractall(target, filter="data")
            except TypeError:
                with tarfile.open(_NODE_ARCHIVE, "r:gz") as archive:
                    archive.extractall(target)
        if not exe.is_file():
            raise RuntimeError("could not unpack the vendored node runtime")
        exe.chmod(0o755)
        return str(exe)

    def _route(self, source):
        """--plugin value for the vendored engine, or None to let it auto-detect."""
        version = header_version(source)
        if version and version[0] == "14" and version[1] is not None:
            if version[1] in _V14_PLUGINS:
                return _V14_PLUGINS[version[1]]
            if version[1] >= 10:
                return "luraph_v14_9"
            return None  # older v14.x: the Node engine's v14 family + fallback chain
        if version and version[0] == "15":
            return "luraph_v15"
        return None

    def deobfuscate(self, job):
        if not SCRIPT.is_file():
            raise RuntimeError("the vendored Luraph engine is missing deob.js")
        out_path = Path(job.path(".all.lua"))
        cmd = [self._node(), str(SCRIPT)]
        route = self._route(job.source)
        if route:
            cmd += ["--plugin", route]
        timeout = int(getattr(job.args, "timeout", 0) or 600)
        timeout = max(60, min(timeout, 1500))
        cmd += ["--timeout", str(timeout), "-o", str(out_path), str(job.source_path)]
        env = dict(os.environ)
        env["PYTHON_BIN"] = sys.executable or "python3"
        env["LURAPH_OPEN_SOURCE_ROOT"] = str(ROOT)
        env["NODE_OPTIONS"] = "--max-old-space-size=6144"
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(ROOT),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout + 180,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                "Luraph (All Versions) exceeded the %ds engine limit." % (timeout + 180)
            )
        tail = (proc.stdout or b"").decode("utf-8", "replace")[-1800:]
        if proc.returncode != 0:
            raise RuntimeError("Luraph engine failed:\n" + tail)
        if not out_path.is_file():
            raise RuntimeError(
                "Luraph engine produced no output for this file:\n" + tail
            )
        return str(out_path)
