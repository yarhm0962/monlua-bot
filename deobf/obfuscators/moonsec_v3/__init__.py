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



def _long_level(text, i):
    """text[i] is '['. Return (level, index_after_open) for a long bracket, else (None, i)."""
    n = len(text)
    if i >= n or text[i] != "[":
        return None, i
    j = i + 1
    while j < n and text[j] == "=":
        j += 1
    if j < n and text[j] == "[":
        return j - i - 1, j + 1
    return None, i


def scan_source(text):
    """Walk the source like a Lua lexer and report two corruption signals.

    A bare backslash is never valid Lua outside a literal. Seeing one followed
    by a quote is the signature of an over-escaped dump (quotes stored as \" ),
    seeing any other stray backslash is plain corruption. Returns a dict with
    the counts and the text with stray backslashes dropped.
    """
    out = []
    strays = 0
    escaped_quote = False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "-" and text[i:i + 2] == "--":
            lvl, after = _long_level(text, i + 2)
            if lvl is not None:
                close = "]" + "=" * lvl + "]"
                j = text.find(close, after)
                end = n if j == -1 else j + len(close)
                out.append(text[i:end]); i = end; continue
            j = text.find("\n", i)
            if j == -1:
                out.append(text[i:]); break
            out.append(text[i:j]); i = j; continue
        if c == "[":
            lvl, after = _long_level(text, i)
            if lvl is not None:
                close = "]" + "=" * lvl + "]"
                j = text.find(close, after)
                end = n if j == -1 else j + len(close)
                out.append(text[i:end]); i = end; continue
            out.append(c); i += 1; continue
        if c in ('"', "'"):
            quote = c
            out.append(c); i += 1
            while i < n:
                ch = text[i]
                if ch == "\\" and i + 1 < n:
                    out.append(ch); out.append(text[i + 1]); i += 2; continue
                out.append(ch); i += 1
                if ch == quote:
                    break
            continue
        if c == "\\":
            strays += 1
            if text[i + 1:i + 2] in ('"', "'"):
                escaped_quote = True
            i += 1
            continue
        out.append(c); i += 1
    return {"cleaned": "".join(out), "strays": strays, "escaped_quote": escaped_quote}


_ESCAPES = {"\\": "\\", '"': '"', "'": "'", "/": "/", "b": "\b",
            "f": "\f", "n": "\n", "r": "\r", "t": "\t"}


def unescape_source(text):
    """Undo one pass of JSON-style escaping over the whole file."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "u" and re.match(r"[0-9a-fA-F]{4}", text[i + 2:i + 6]):
                out.append(chr(int(text[i + 2:i + 6], 16))); i += 6; continue
            if nxt in _ESCAPES:
                out.append(_ESCAPES[nxt]); i += 2; continue
        out.append(c); i += 1
    return "".join(out)


def strip_stray_backslashes(text):
    return scan_source(text)["cleaned"]


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
        with open(job.source_path, encoding="utf-8", errors="replace") as f:
            source = f.read()
        scan = scan_source(source)
        candidates = []
        if scan["escaped_quote"]:
            candidates.append(strip_stray_backslashes(unescape_source(source)))
        candidates.append(source)
        if scan["strays"] and scan["cleaned"] != source:
            candidates.append(scan["cleaned"])
        out_path = job.path(".moonsec.dis")
        env = dict(os.environ, DOTNET_SYSTEM_GLOBALIZATION_INVARIANT="1", DOTNET_CLI_TELEMETRY_OPTOUT="1")
        cand_path = job.path(".moonsec_in.lua")
        best_error = "no diagnostic output"
        for cand in candidates:
            with open(cand_path, "w", encoding="utf-8") as f:
                f.write(cand)
            try:
                proc = subprocess.run(
                    [exe, "-dis", "-i", cand_path, "-o", out_path],
                    capture_output=True, timeout=job.args.timeout, env=env)
            except subprocess.TimeoutExpired:
                sys.exit("[!] MoonSec V3 deobfuscation timed out after %ds" % job.args.timeout)
            if proc.returncode == 0 and os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
                break
            text = (proc.stderr or proc.stdout or b"").decode("utf-8", "replace")
            best_error = "no diagnostic output"
            for line in text.splitlines():
                if "Exception" in line or "error" in line.lower():
                    best_error = line.strip()[:300]
                    break
            else:
                if text.strip():
                    best_error = text.strip()[:300]
        else:
            sys.exit("[!] MoonSec V3 deobfuscation failed: %s" % best_error)
        with open(out_path, encoding="utf-8", errors="replace") as f:
            dis = f.read()
        header = (job.credit_header() +
                  "-- Devirtualized MoonSec V3 bytecode, as a readable disassembly\n"
                  "-- MoonSec V3 does not keep the original source; this is the recovered program\n")
        return job.write(job.path(".moonsec_dis.txt"), header + dis + "\n")
