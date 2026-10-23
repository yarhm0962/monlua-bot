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
        from obfuscators.extra_families import leading_lua_comments, strip_lua_comments, strip_lua_strings
        # A precise vendor banner is strong evidence, but a mere URL/name mention
        # is corroboration only and must agree with executable-code shape.
        leading_comments = leading_lua_comments(source)[:4000]
        if HEADER.search(leading_comments):
            self.last_evidence = ["Centurion vendor header (centurion.best)"]
            return 1.0
        code = strip_lua_comments(source)
        structure = strip_lua_strings(code)
        domain_hint = "centurion.best" in leading_comments.lower()
        c3 = len(re.findall(r"\bc3\[", structure))
        fz = len(re.findall(r"function\(Z\)", structure))
        evidence = []
        if c3 >= 50 and fz >= 20:
            evidence.append("%d c3[N] refs + %d function(Z) factories" % (c3, fz))
            if domain_hint:
                evidence.append("centurion.best vendor-domain corroboration")
            self.last_evidence = evidence
            return 0.95 if domain_hint else 0.85
        if c3 >= 20 and fz >= 10:
            evidence.append("%d c3[N] refs + %d function(Z) factories" % (c3, fz))
            if domain_hint:
                evidence.append("centurion.best vendor-domain corroboration")
            self.last_evidence = evidence
            return 0.85 if domain_hint else 0.7
        if c3 >= 5 or fz >= 5:
            evidence.append("%d c3[N] refs + %d function(Z) factories (weak shape)" % (c3, fz))
            if domain_hint:
                evidence.append("centurion.best vendor-domain corroboration")
            self.last_evidence = evidence
            return 0.7 if domain_hint else 0.5
        if domain_hint:
            self.last_evidence = ["centurion.best appears in a leading comment, but code structure did not corroborate it"]
            return 0.6
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
