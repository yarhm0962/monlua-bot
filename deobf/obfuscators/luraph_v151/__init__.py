"""Luraph v15.1 detection and routing to the shared v15.1 Node pipeline."""
import re

from obfuscators.luraph_v15 import HEADER, HEADER_ANY, LPH_RX, SLOT_RX, find_vm_chunk


class LuraphV151:
    name = "luraph_v151"
    label = "Luraph v15.1"
    doc = "LURAPH.md"

    def detect(self, source, analysis=None):
        from obfuscators.extra_families import LuaAnalysis

        analysis = analysis or LuaAnalysis(source)
        comments = analysis.header[:4000]
        structure = analysis.structure

        match = HEADER.search(comments)
        if match:
            major, minor = match.group(1), match.group(2)
            if major == "15" and minor == "1":
                self.last_evidence = ["official Luraph v15.1 header comment"]
                return 1.0
            if major == "15" and minor in (None, "0"):
                self.last_evidence = ["official Luraph v15.0 header; not a v15.1 match"]
                return 0.0
            self.last_evidence = ["official Luraph header states v%s%s" % (
                major, "." + minor if minor is not None else ""
            )]
            return 0.0

        if HEADER_ANY.search(comments):
            version = re.search(r"v?(1[3-6])\.(\d+)", comments, re.I)
            if version:
                major, minor = version.group(1), version.group(2)
                if major == "15" and minor == "1":
                    self.last_evidence = ["rebranded leading Luraph header states v15.1"]
                    return 0.96
                self.last_evidence = ["rebranded Luraph header states v%s.%s, not v15.1" % (major, minor)]
                return 0.0
            self.last_evidence = ["Luraph header found, but its version is not stated"]
            return 0.35

        if re.search(r"luraph", comments, re.I):
            version = re.search(r"v?(1[3-6])\.(\d+)", comments, re.I)
            if version:
                major, minor = version.group(1), version.group(2)
                if major == "15" and minor == "1":
                    self.last_evidence = ["Luraph named in a leading comment with version v15.1"]
                    return 0.96
                self.last_evidence = ["Luraph leading comment states v%s.%s, not v15.1" % (major, minor)]
                return 0.0
            self.last_evidence = ["unversioned Luraph mention in a leading comment"]
            return 0.25

        vm_at = find_vm_chunk(structure)
        if vm_at is not None:
            vm_region = structure[vm_at:vm_at + 200000]
            pragmas = sum(1 for _ in LPH_RX.finditer(vm_region))
            slots = sum(1 for _ in SLOT_RX.finditer(vm_region))
            if pragmas or slots:
                evidence = ["Luraph VM shape found after loader stub; version header is absent"]
                if pragmas:
                    evidence.append("%d LPH VM directives" % pragmas)
                if slots:
                    evidence.append("%d numeric library slots" % slots)
                self.last_evidence = evidence
                return 0.86 if pragmas >= 3 and slots >= 3 else 0.81

        pragmas = sum(1 for _ in LPH_RX.finditer(structure))
        slots = sum(1 for _ in SLOT_RX.finditer(structure))
        if pragmas:
            self.last_evidence = ["%d LPH directives found, but no v15.1-specific VM boundary" % pragmas]
            return 0.55
        if slots:
            self.last_evidence = ["%d numeric library slots found without a versioned VM boundary" % slots]
            return 0.55

        self.last_evidence = []
        return 0.0

    def add_arguments(self, ap):
        return

    def deobfuscate(self, job):
        raise SystemExit(
            "Luraph v15.1 deobfuscation runs through the Node pipeline "
            "(deobf/v151/deob.js); deob.py's Python pipeline handles v15.0."
        )
