"""
moonsec_v3: MoonSec V3 (header "This file was protected with MoonSec V3
by ..."). Notes: MOONSECV3.md. A C# devirtualizer (bin/MoonsecDeobfuscator,
built from tupsutumppu/MoonsecDeobfuscator) parses the script, unfolds its
string/constant decoding and rewrites the VM loader into Lua 5.1 bytecode.
The plugin runs it with -dev, which writes the recovered code as a real
Lua 5.1 bytecode chunk, then decompiles that chunk with vendored unluac
(bin/unluac.jar + bin/jre17.tar.gz, unpacked to /tmp/monlua-jre) so the
output is actual Lua source. If the decompiler is unavailable or rejects
the bytecode, the plugin falls back to the tool's -dis listing.
"""
import os
import re
import shutil
import subprocess
import sys
import tarfile

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


def unwrap_string_dump(text):
    """Recover a script that was dumped inside a string literal.

    Paste sites wrap the whole obfuscated script in print("...") (or a similar
    call) without escaping it, so the wrapper's own quotes are the only
    structure to strip: take the text between the first and last quote.
    Returns the recovered script, or None when the file is not that shape.
    """
    q1 = text.find('"')
    quote = '"'
    if q1 == -1:
        q1 = text.find("'")
        quote = "'"
        if q1 == -1:
            return None
    prefix = text[:q1].rstrip()
    if q1 > 40 or not re.fullmatch(r"[A-Za-z_][\w.]*\(", prefix):
        return None
    q2 = text.rfind(quote)
    if q2 <= q1:
        return None
    inner = text[q1 + 1:q2]
    if not HEADER.search(inner[:600]):
        return None
    return inner

def strip_stray_backslashes(text):
    return scan_source(text)["cleaned"]


_INSTR = re.compile(
    r"^(\t*)\[\s*(\d+)\]\t+\s*([A-Za-z_]\w*)\t+\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\t?(.*)$")


def beautify_dis(text):
    """Tidy the tool's tab-and-pipe instruction table into aligned columns."""
    out = []
    for line in text.splitlines():
        m = _INSTR.match(line)
        if m:
            indent, idx, op, a, b, c, code = m.groups()
            out.append("%s    [%5d] %-14s %s %s %s   %s" % (
                indent.replace("\t", "    "), int(idx), op, a.rjust(4), b.rjust(4), c.rjust(4), code.strip()))
        elif line.lstrip().startswith("function "):
            if out and out[-1].strip():
                out.append("")
            out.append(line)
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def _find_java():
    """A Java runtime for unluac: system java first, else the vendored JRE."""
    sys_java = shutil.which("java")
    if sys_java:
        return sys_java
    base = os.path.join("/tmp", "monlua-jre")
    java = os.path.join(base, "jdk-17.0.20.1+1-jre", "bin", "java")
    if os.path.isfile(java):
        return java
    archive = os.path.join(ROOT, "bin", "jre17.tar.gz")
    if not os.path.isfile(archive):
        return None
    try:
        if os.path.isdir(base) and not os.listdir(base):
            os.rmdir(base)               # clean a failed extract before retrying
        os.makedirs(base, exist_ok=True)
        with tarfile.open(archive, "r:gz") as t:
            try:
                t.extractall(base, filter="data")
            except TypeError:            # pre-3.12 tarfile has no filter=
                t.extractall(base)
    except Exception:
        return None
    return java if os.path.isfile(java) else None


def _decompile_with_unluac(dev_path, job):
    """unluac turns the recovered Lua 5.1 bytecode back into Lua source."""
    java = _find_java()
    if not java:
        return None
    jar = os.path.join(ROOT, "bin", "unluac.jar")
    if not os.path.isfile(jar):
        return None
    try:
        proc = subprocess.run(
            [java, "-Xmx256m", "-XX:+UseSerialGC", "-jar", jar, "--nodebug", dev_path],
            capture_output=True, timeout=job.args.timeout)
    except subprocess.TimeoutExpired:
        return None
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    lua = proc.stdout.decode("utf-8", "replace")
    if not lua.strip():
        return None
    return lua


_DEC_CALL = re.compile(r'\br\((?:\d+|0x[0-9a-fA-F]+)\s*,\s*"[^"]{60,}"')
_ESC8 = re.compile(r"\\4\\8")


class MoonsecV3(Obfuscator):
    name = "moonsec_v3"
    label = "MoonSec V3"
    doc = "MOONSECV3.md"

    def detect(self, source):
        from obfuscators.extra_families import leading_lua_comments, strip_lua_comments
        header = leading_lua_comments(source)[:4000]
        if HEADER.search(header):
            self.last_evidence = ["MoonSec V3 header comment"]
            return 1.0
        if "moonsec v3" in header.lower():
            self.last_evidence = ["MoonSec V3 version mention in the leading header comment"]
            return 0.8
        # Structural signals are counted on comment-stripped code. String
        # literals remain intact because MoonSec's decoder calls use them.
        head = strip_lua_comments(source).lstrip()
        calls = sum(1 for _ in _DEC_CALL.finditer(head))
        esc8 = sum(1 for _ in _ESC8.finditer(head))
        if calls >= 5:
            conf = 0.8 if calls < 25 else 0.85
            ev = ["%d string-decoder call sites (%.1f per KB, need 5)" % (calls, 1000.0 * calls / max(1, len(source)))]
            if esc8:
                conf = min(0.9, conf + 0.05)
                ev.append("%d encoded-constant strings" % esc8)
            self.last_evidence = ev
            return conf
        if calls:
            self.last_evidence = ["%d string-decoder call sites (need 5 for a confident match)" % calls]
            return 0.65 if calls >= 2 else 0.5
        if esc8 >= 5:
            self.last_evidence = ["%d encoded-constant strings, no decoder calls" % esc8]
            return 0.65
        if esc8:
            self.last_evidence = ["%d encoded-constant string(s), no decoder calls" % esc8]
            return 0.55
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        exe = os.path.join(ROOT, "bin", "MoonsecDeobfuscator")
        if not os.path.isfile(exe) or not os.access(exe, os.X_OK):
            sys.exit("[!] the MoonSec V3 binary is missing (deobf/bin/MoonsecDeobfuscator)")
        with open(job.source_path, encoding="utf-8", errors="replace") as f:
            source = f.read()
        unwrap = unwrap_string_dump(source)
        candidates = []
        if unwrap is not None:
            base = unwrap.rstrip()
            if base.endswith("."):
                candidates.append(base[:-1].rstrip())
            candidates.append(base)
            candidates.append(unescape_source(base))
        scan = scan_source(source)

        if scan["escaped_quote"]:
            candidates.append(strip_stray_backslashes(unescape_source(source)))
        candidates.append(source)
        if scan["strays"] and scan["cleaned"] != source:
            candidates.append(scan["cleaned"])
        env = dict(os.environ, DOTNET_SYSTEM_GLOBALIZATION_INVARIANT="1", DOTNET_CLI_TELEMETRY_OPTOUT="1")
        cand_path = job.path(".moonsec_in.lua")
        dev_path = job.path(".moonsec.bytecode")
        best_error = "no diagnostic output"

        def _run(mode, out_path, cand):
            nonlocal best_error
            with open(cand_path, "w", encoding="utf-8") as f:
                f.write(cand)
            try:
                proc = subprocess.run(
                    [exe, mode, "-i", cand_path, "-o", out_path],
                    capture_output=True, timeout=job.args.timeout, env=env)
            except subprocess.TimeoutExpired:
                sys.exit("[!] MoonSec V3 deobfuscation timed out after %ds" % job.args.timeout)
            if proc.returncode == 0 and os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
                return True
            text = (proc.stderr or proc.stdout or b"").decode("utf-8", "replace")
            best_error = "no diagnostic output"
            for line in text.splitlines():
                if "Exception" in line or "error" in line.lower():
                    best_error = line.strip()[:300]
                    break
            else:
                if text.strip():
                    best_error = text.strip()[:300]
            return False

        # Pass 1: recover the bytecode (-dev). Pass 2: decompile it back to
        # real Lua source with unluac. Only if that rail is unavailable do we
        # fall back to the tool's -dis listing.
        for cand in candidates:
            if _run("-dev", dev_path, cand):
                lua = _decompile_with_unluac(dev_path, job)
                if lua is not None:
                    return job.write(job.path(".moonsec.lua"), job.credit_header() + lua + "\n")
                break                       # bytecode ok, decompiler failed -> listing
        else:
            dev_path = None
        if dev_path is None:
            out_path = job.path(".moonsec.dis")
            for cand in candidates:
                if _run("-dis", out_path, cand):
                    break
            else:
                sys.exit("[!] MoonSec V3 deobfuscation failed: %s" % best_error)
            with open(out_path, encoding="utf-8", errors="replace") as f:
                dis = f.read()
            header = job.credit_header()
            return job.write(job.path(".moonsec_dis.txt"), header + beautify_dis(dis) + "\n")
        # decompiler failed but bytecode exists: still produce the listing
        out_path = job.path(".moonsec.dis")
        if _run("-dis", out_path, candidates[0]):
            with open(out_path, encoding="utf-8", errors="replace") as f:
                dis = f.read()
            header = job.credit_header()
            return job.write(job.path(".moonsec_dis.txt"), header + beautify_dis(dis) + "\n")
        sys.exit("[!] MoonSec V3 deobfuscation failed: %s" % best_error)
