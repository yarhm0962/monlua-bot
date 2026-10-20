"""
moonsec_v3: MoonSec V3 (header "This file was protected with MoonSec V3
by ..."). Notes: MOONSECV3.md. A C# devirtualizer (bin/MoonsecDeobfuscator,
built from tupsutumppu/MoonsecDeobfuscator) parses the script, unfolds its
string/constant decoding and rewrites the VM loader into Lua 5.1 bytecode.
The plugin runs it and writes the bytecode back as a readable disassembly
(the original source is gone in MoonSec V3; this is what the tool produces).
"""
import os
import re
import subprocess
import sys

from obfuscators.base import Obfuscator

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))     # deobf/ (bin/)
HEADER = re.compile(r"this file was protected with moonsec\s*v3\b", re.I)


class MoonsecV3(Obfuscator):
    name = "moonsec_v3"
    label = "MoonSec V3"
    doc = "MOONSECV3.md"

    def detect(self, source):
        if HEADER.search(source[:600]):
            return 1.0
        if "moonsec v3" in source[:600].lower():
            return 0.8
        return 0.0

    def deobfuscate(self, job):
        exe = os.path.join(ROOT, "bin", "MoonsecDeobfuscator")
        if not os.path.isfile(exe) or not os.access(exe, os.X_OK):
            sys.exit("[!] the MoonSec V3 binary is missing (deobf/bin/MoonsecDeobfuscator)")
        out_path = job.path(".moonsec.dis")
        env = dict(os.environ, DOTNET_SYSTEM_GLOBALIZATION_INVARIANT="1", DOTNET_CLI_TELEMETRY_OPTOUT="1")
        try:
            proc = subprocess.run(
                [exe, "-dis", "-i", job.source_path, "-o", out_path],
                capture_output=True, timeout=job.args.timeout, env=env)
        except subprocess.TimeoutExpired:
            sys.exit("[!] MoonSec V3 deobfuscation timed out after %ds" % job.args.timeout)
        if proc.returncode != 0 or not os.path.isfile(out_path) or os.path.getsize(out_path) == 0:
            text = (proc.stderr or proc.stdout or b"").decode("utf-8", "replace")
            detail = ""
            for line in text.splitlines():
                if "Exception" in line or "error" in line.lower():
                    detail = line.strip()[:300]
                    break
            sys.exit("[!] MoonSec V3 deobfuscation failed: %s"
                     % (detail or text.strip()[:300] or "exit code %d" % proc.returncode))
        with open(out_path, encoding="utf-8", errors="replace") as f:
            dis = f.read()
        header = (job.credit_header() +
                  "-- Devirtualized MoonSec V3 bytecode, as a readable disassembly\n"
                  "-- MoonSec V3 does not keep the original source; this is the recovered program\n")
        return job.write(job.path(".moonsec_dis.txt"), header + dis + "\n")
