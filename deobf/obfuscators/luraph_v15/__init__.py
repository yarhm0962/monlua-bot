"""Luraph v15 plugin: devirtualizer + behaviour trace (notes: LURAPH.md)."""
import re
import sys

from obfuscators.base import Obfuscator

HEADER = re.compile(r"This file was protected using Luraph Obfuscator v(\d+)(?:\.(\d+))?")
# rebranded/repacked Luraph builds keep the VM but reword the header ("obfuscated by"
# "Luraph Skid Lol", custom marketing URLs), so match the brand without requiring a version.
HEADER_ANY = re.compile(r"(?:protected using|obfuscated by|generated using)\s+Luraph\b", re.I)
HEADER_LINE = re.compile(r"\s*--[ \t]*This file was protected using Luraph Obfuscator v[\d.]+[ \t]*"
                         r"\[https?://lura\.ph/?\]")
LPH_RX = re.compile(r"\bLPH_(?:NO_VIRTUALIZE|JIT|CRASH|ENCFUNC|ENCSTR|DECFUNC|DECSTR|ENABLE_CHECKS?)\b")
SLOT_RX = re.compile(r"\[\d+\]=(?:bit32|buffer|string|table|math)\.\w+")


class LuraphV15(Obfuscator):
    name = "luraph_v15"
    label = "Luraph v15"
    doc = "LURAPH.md"

    def detect(self, source):
        # headers can be a long multi-line comment block; search the first 4 KB
        m = HEADER.search(source[:4000])
        if m:
            self.last_evidence = ["official Luraph header comment (v%s)" % m.group(1)]
            return 1.0 if m.group(1) == "15" else 0.3     # other versions: probably close, not verified
        if HEADER_ANY.search(source[:4000]):
            # Luraph brand without the official version line (repacked builds): same VM.
            self.last_evidence = ["rebranded Luraph header (brand, no official version line)"]
            return 0.95
        # header stripped: v15's shape is `return setmetatable({...VM object...}, ...)`
        # with numeric-keyed library slots (`[75]=bit32.rrotate`) and `LPH` markers.
        # Skip leading comment lines first: a rebranded header comment must not
        # hide the VM shape behind it.
        stripped = re.sub(r"^(\s*--[^\n]*(\n|$))+", "", source.lstrip())
        # every structural signal is counted across the WHOLE file, not a window
        pragmas = len(LPH_RX.findall(source))
        slots = sum(1 for _ in SLOT_RX.finditer(source))
        head = stripped[:2000]
        # code-shape signals, not comment-based: the VM object opens with
        # `return setmetatable({...})`; its library slots and LPH markers can
        # sit deep in an 800 KB file
        if head.startswith("return setmetatable({") and (slots or pragmas):
            ev = ["Luraph VM shape: setmetatable VM object"]
            if slots:
                ev.append("%d numeric library slots anywhere in the file" % slots)
            if pragmas:
                ev.append("%d LPH pragmas anywhere in the file" % pragmas)
            self.last_evidence = ev
            return 0.85 if (pragmas >= 3 and slots >= 3) else 0.8
        # LPH_* markers alone (LPH_NO_VIRTUALIZE, LPH_JIT, LPH_ENCFUNC, ...) are
        # Luraph's own pragmas: real obfuscator output, no header needed.
        if pragmas:
            first = LPH_RX.search(source).group(0)
            self.last_evidence = ["%s and %d LPH pragmas total (Luraph's own directives)" % (first, pragmas)]
            return 0.85
        if slots >= 3:
            # numeric library-slot tables are a VM artifact, rare in hand-written code:
            # honest "possible match", never a confident verdict
            self.last_evidence = ["%d numeric library slots (Luraph VM artifact, no header/VM shape)" % slots]
            return 0.55
        self.last_evidence = []
        return 0.0

    def add_arguments(self, ap):
        g = ap.add_argument_group("Luraph v15")
        g.add_argument("--no-hooks", action="store_true",
                       help="do not instrument VM functions (no anti-tamper trap attribution, no lifting)")
        g.add_argument("--max-runs", type=int, default=12, help="maximum number of trace runs (trap reruns)")
        g.add_argument("--devirt-rounds", type=int, default=200,
                       help="max lift + constant-request rounds (default 200; stops early when no new "
                            "constants turn up)")

    def deobfuscate(self, job):
        from obfuscators.luraph_v15 import driver
        fixed = restore_header_newline(job.source)
        if fixed != job.source:
            # the copy keeps the input's name (Path2D cache, messages use job.input)
            print("[*] header comment ran into the code (lost newline): split it", file=sys.stderr)
            job.source = fixed
            job.source_path = job.write(job.path(".src.lua"), fixed, encoding="latin-1")
        return driver.run(job)


def restore_header_newline(source):
    """Pasted copies (e.g. Discord's message.txt) can lose the newline after
    the `-- This file was protected ... [https://lura.ph/]` line, which turns
    the whole script into that comment. Put it back."""
    m = HEADER_LINE.match(source)
    if m and source[m.end():m.end() + 1] not in ("", "\n", "\r"):
        return source[:m.end()] + "\n" + source[m.end():].lstrip(" \t")
    return source
