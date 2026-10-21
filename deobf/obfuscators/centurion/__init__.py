"""
centurion: the Centurion obfuscator (header "This file was obfuscated using
Centurion v6[.1] | https://centurion.best/"). Runs the vendored centurion.py
(deobf/centurion/) fully offline:
  v6 shape   -> static payload-factory lift (stage1), no game needed.
  v6.1 shape -> envlog sandbox attempt with frozen answer packs; on the junk
                branch the maximal readable reconstruction (stages, strings,
                empty stubs, never faked data) is returned instead of a
                pretend-clean output.
"""
import json
import re
import os
import shutil
import subprocess
import sys

from obfuscators.base import Obfuscator

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "centurion"))
DEOBF_DIR = os.path.dirname(TOOL_DIR)  # deobf/: harness.py, envlog.luau, bin/
HEADER = re.compile(r"obfuscated using Centurion v?6", re.I)
SHAPE = re.compile(r"\bc3\[\d+\]\s*=\s*function\(Z\)")


class Centurion(Obfuscator):
    name = "centurion"
    label = "Centurion"
    doc = "CENTURION.md"

    def detect(self, source):
        head = source[:4000]
        if HEADER.search(head):
            self.last_evidence = ["Centurion header (centurion.best)"]
            return 0.95
        n = len(SHAPE.findall(source[:20000]))
        if n >= 20:
            self.last_evidence = ["%d c3[N]=function(Z) payload factories" % n]
            return 0.55
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        env = dict(os.environ)
        env["CENT_SANDBOX"] = DEOBF_DIR
        env["CENT_LUAU_LUAU"] = os.path.join(DEOBF_DIR, "bin", "luau")
        env["CENT_LUAU_LUAU_AST"] = os.path.join(DEOBF_DIR, "bin", "luau-ast")
        env["CENT_LUAU_LUAU_COMPILE"] = os.path.join(DEOBF_DIR, "bin", "luau")
        env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
        timeout = int(getattr(job.args, "timeout", 0) or 0) or 600
        timeout = max(60, timeout - 15)
        cmd = [sys.executable, os.path.join(TOOL_DIR, "centurion.py"),
               "deobfuscate", job.source_path, "--out-dir", job.outdir]
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            raise RuntimeError("Centurion run exceeded the %ds job timeout" % timeout)
        out = proc.stdout.decode("utf-8", "replace")
        if proc.returncode not in (0, 3):
            err = (proc.stderr.decode("utf-8", "replace") or out)[-400:]
            raise RuntimeError("centurion.py failed: %s" % err.strip())
        res = None
        dec = json.JSONDecoder()
        idx = 0
        while True:
            j = out.find("{", idx)
            if j < 0:
                break
            try:
                obj, end = dec.raw_decode(out[j:])
                if isinstance(obj, dict) and "verdict" in obj:
                    res = obj
                idx = j + 1
            except Exception:
                idx = j + 1
        if res is None:
            raise RuntimeError("centurion.py produced no result: %s" % out[-300:])
        files = res.get("files") or []
        if res.get("verdict") == "DEOBFUSCATED":
            pick = None
            for f in files:
                if f.endswith("_stage1.lua"):
                    pick = f
            if not pick:
                for f in files:
                    if f.endswith("_beautified.lua"):
                        pick = f
            if not pick and files:
                pick = files[0]
        else:
            pick = res.get("maximal") or (files[-1] if files else None)
        if not pick or not os.path.exists(pick):
            raise RuntimeError("centurion.py returned no usable output (%s)"
                               % res.get("reason", ""))
        dest = job.path("_cent_result.lua")
        shutil.copyfile(pick, dest)
        print("[+] centurion: %s (%s)" % (res.get("verdict"), os.path.basename(pick)),
              file=sys.stderr)
        return dest
