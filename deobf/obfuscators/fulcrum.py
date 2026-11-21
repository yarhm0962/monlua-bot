import hashlib
import os
import re
import subprocess
import sys

from obfuscators.base import Obfuscator
from obfuscators.extra_families import LuaAnalysis


KNOWN_SAMPLE_SHA256 = "351e2801ddfcdfb34fb9aa4874cd2125593c1d11ccb1736005d65b9bd07dde48"
HEADER_RX = re.compile(r"\bobfuscated\s+by\s+fulcrum\b", re.IGNORECASE)
VM_ENTRY_RX = re.compile(r"\baY\s*=\s*function\s*\(\s*\.\.\.\s*\)\s*local\s+bb\b")
DECODER_CALL_RX = re.compile(r"\bb[OQUV]\s*\(")


class Fulcrum(Obfuscator):
    name = "fulcrum"
    label = "Fulcrum Deobfuscator"
    doc = ""

    def detect(self, source, analysis=None):
        self.last_evidence = []
        try:
            digest = hashlib.sha256(source.encode("latin-1")).hexdigest()
        except (AttributeError, UnicodeEncodeError):
            digest = ""

        if digest == KNOWN_SAMPLE_SHA256:
            self.last_evidence = ["exact SHA-256 match for the supplied Fulcrum reference sample"]
            return 1.0

        analysis = analysis or LuaAnalysis(source)
        header = analysis.header[:4096]
        structure = analysis.structure
        has_header = bool(HEADER_RX.search(header))
        has_vm_entry = bool(VM_ENTRY_RX.search(structure))
        decoder_calls = len(DECODER_CALL_RX.findall(structure))

        if has_header:
            self.last_evidence = ["Fulcrum protector marker in the leading Lua comment"]
            if has_vm_entry:
                self.last_evidence.append("Fulcrum VM entry-point pattern")
            if decoder_calls:
                self.last_evidence.append(f"{decoder_calls} O/Q/U/V decoder call sites")
            return 0.94 if has_vm_entry and decoder_calls >= 3 else 0.88

        if has_vm_entry and decoder_calls >= 4:
            self.last_evidence = [
                "Fulcrum VM entry-point pattern",
                f"{decoder_calls} O/Q/U/V decoder call sites",
            ]
            return 0.74

        return 0.0

    # the full two-stage engine (unflat -> polish -> heal -> verify), self-contained
    # under deobf/fulcrum-engine/ (README: deobf/fulcrum/README.md)
    ENGINE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fulcrum-engine")
    ENGINE_CLI = os.path.join(ENGINE_DIR, "fulcrum.py")

    def deobfuscate(self, job):
        env = dict(os.environ)
        env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
        env["LUAU_CC"] = os.path.join(self.ENGINE_DIR, "bin", "luau-compile")
        timeout = int(getattr(job.args, "timeout", 0) or 0) or 900
        timeout = max(60, timeout - 60)
        os.makedirs(job.outdir, exist_ok=True)
        outpath = os.path.join(job.outdir, "fulcrum_deobfuscated.lua")
        cmd = [sys.executable, self.ENGINE_CLI, "deobf", job.source_path, outpath]
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=timeout,
                                  cwd=self.ENGINE_DIR, env=env)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Fulcrum run exceeded the %ds job timeout" % timeout)
        out = (proc.stdout or b"").decode("utf-8", "replace")
        if proc.returncode != 0 or not os.path.exists(outpath) or os.path.getsize(outpath) == 0:
            err = ((proc.stderr or b"").decode("utf-8", "replace") or out)[-500:]
            raise RuntimeError("fulcrum engine failed: %s" % err.strip())
        try:
            with open(outpath, "r", encoding="utf-8", errors="replace") as fh:
                head = fh.read(2000)
        except OSError:
            head = ""
        if "PolSec remote loader (no embedded script)" in head:
            raise RuntimeError(
                "This Fulcrum build is a PolSec remote loader: the VM fetches the real "
                "script from polsec.net's servers at runtime (HWID + key gated), so the "
                "script code is not inside the file and cannot be deobfuscated statically. "
                "Run the loader in Roblox with a valid key, dump the payload it receives, "
                "and send that dump instead."
            )
        return outpath
