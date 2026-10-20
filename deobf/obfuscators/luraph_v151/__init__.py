"""Luraph v15.1 detection: same VM family as v15, with the version resolved
where the file actually states it. Shares signals with ../luraph_v15."""
import re

from obfuscators.luraph_v15 import HEADER, HEADER_ANY, LPH_RX, SLOT_RX, LuraphV15


class LuraphV151(LuraphV15):
    name = "luraph_v151"
    label = "Luraph v15.1"
    doc = "LURAPH.md"

    def detect(self, source):
        m = HEADER.search(source[:4000])
        if m:
            minor = m.group(2)
            if minor is not None and minor != "0":
                self.last_evidence = ["official Luraph header comment (v15.%s)" % minor]
                return 1.0
            self.last_evidence = []          # v15.0.x belongs to the v15 engine
            return 0.0
        if HEADER_ANY.search(source[:4000]):
            # repacked builds reword the header and drop the version line; the
            # VM is the same either way. v15.1 is the current release of the
            # 15 line, so rebranded files report as v15.1 while the v15 engine
            # stays one point below on the very same signal.
            self.last_evidence = ["rebranded Luraph header (brand, no version line; reported as v15.1)"]
            return 0.96
        # header fully stripped: same shape signals as v15, one point above so
        # the family reports under v15.1
        stripped = re.sub(r"^(\s*--[^\n]*(\n|$))+", "", source.lstrip())
        pragmas = len(LPH_RX.findall(source))
        slots = sum(1 for _ in SLOT_RX.finditer(source))
        head = stripped[:2000]
        if head.startswith("return setmetatable({") and (slots or pragmas):
            self.last_evidence = ["Luraph VM shape: setmetatable VM object (version not stated; reported as v15.1)"]
            return 0.86 if (pragmas >= 3 and slots >= 3) else 0.81
        if pragmas:
            first = LPH_RX.search(source).group(0)
            self.last_evidence = [
                "%s and %d LPH pragmas total (version not stated; reported as v15.1)" % (first, pragmas)]
            return 0.86
        if slots >= 3:
            self.last_evidence = ["%d numeric library slots (Luraph VM artifact, no header/VM shape)" % slots]
            return 0.56
        self.last_evidence = []
        return 0.0

    def add_arguments(self, ap):
        # the v15.1 engine runs through the Node pipeline (bot.py routes it
        # there directly); the v15 engine already registers its own options,
        # and adding the same ones twice would crash argparse
        return

    def deobfuscate(self, job):
        raise SystemExit(
            "Luraph v15.1 deobfuscation runs through the Node pipeline "
            "(deobf/v151/deob.js); deob.py's Python pipeline handles v15.0.")
