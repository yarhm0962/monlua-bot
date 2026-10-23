"""Luraph v15.1 detection: same VM family as v15, with the version resolved
where the file actually states it. Shares signals with ../luraph_v15."""
import re

from obfuscators.luraph_v15 import HEADER, HEADER_ANY, LPH_RX, SLOT_RX, LuraphV15


class LuraphV151(LuraphV15):
    name = "luraph_v151"
    label = "Luraph v15.1"
    doc = "LURAPH.md"

    def detect(self, source):
        from obfuscators.extra_families import leading_lua_comments, strip_lua_comments, strip_lua_strings
        comments = leading_lua_comments(source)
        code = strip_lua_comments(source)
        structure = strip_lua_strings(code)
        m = HEADER.search(comments[:4000])
        if m:
            minor = m.group(2)
            if minor is not None and minor != "0":
                self.last_evidence = ["official Luraph header comment (v15.%s)" % minor]
                return 1.0
            self.last_evidence = []          # v15.0.x belongs to the v15 engine
            return 0.0
        if HEADER_ANY.search(comments[:4000]):
            vm = re.search(r"v?(1[3-6])\.(\d+)", comments[:4000], re.I)
            if vm and vm.group(1) != "15":
                self.last_evidence = ["Luraph header states a different version (v%s.%s)" % (vm.group(1), vm.group(2))]
                return 0.2
            if vm and vm.group(1) == "15" and vm.group(2) == "0":
                self.last_evidence = ["Rebranded Luraph v15.0 header; not a v15.1 match"]
                return 0.0
            if vm:
                self.last_evidence = ["Rebranded Luraph header with version v15.%s" % vm.group(2)]
                return 0.92
            self.last_evidence = ["Rebranded Luraph header without a version line; v15.1 is a tentative family match"]
            return 0.84
        if re.search(r"luraph", comments[:4000], re.I):
            vm = re.search(r"v?(1[3-6])\.(\d+)", comments[:4000], re.I)
            if vm and vm.group(1) == "15" and vm.group(2) != "0":
                self.last_evidence = ["Luraph named in a leading comment with version v15.%s" % vm.group(2)]
                return 1.0
            if vm and vm.group(1) == "15":
                self.last_evidence = ["Luraph v15 family/version mentioned in a leading comment"]
                return 0.0
            if vm:
                self.last_evidence = ["Luraph mentioned with a different version (v%s.%s)" % (vm.group(1), vm.group(2))]
                return 0.2
            self.last_evidence = ["Luraph named in a leading comment without a validated version/banner"]
            return 0.62
        # header fully stripped: same shape signals as v15, one point above so
        # the family reports under v15.1
        stripped = structure.lstrip()
        pragmas = len(LPH_RX.findall(structure))
        slots = sum(1 for _ in SLOT_RX.finditer(structure))
        head = stripped[:2000]
        if head.startswith("return setmetatable({") and (slots or pragmas):
            self.last_evidence = ["Luraph VM shape: setmetatable VM object (version not stated; reported as v15.1)"]
            return 0.86 if (pragmas >= 3 and slots >= 3) else 0.81
        if pragmas:
            first = LPH_RX.search(structure).group(0)
            self.last_evidence = [
                "%s and %d LPH pragmas total (version not stated; reported as v15.1)" % (first, pragmas)]
            return 0.86
        if slots >= 1:
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
