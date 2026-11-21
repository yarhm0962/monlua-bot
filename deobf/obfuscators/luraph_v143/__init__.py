"""Luraph v14.3 detection and the v14.3 recovery pipeline (research toolkit)."""
import importlib
import os
import re
import sys

from obfuscators.luraph_v15 import HEADER, HEADER_ANY

_BLOB_RX = re.compile(r'x\("((?:[^"\\]|\\.)*)",\s*0[xX]5\)')


class LuraphV143:
    name = "luraph_v143"
    label = "Luraph v14.3"
    doc = "LURAPH.md"

    def detect(self, source, analysis=None):
        from obfuscators.extra_families import LuaAnalysis

        analysis = analysis or LuaAnalysis(source)
        comments = analysis.header[:4000]

        match = HEADER.search(comments)
        if match:
            major, minor = match.group(1), match.group(2)
            if major == "14" and minor == "3":
                self.last_evidence = ["official Luraph v14.3 header comment"]
                return 1.0
            if major == "14":
                self.last_evidence = ["official Luraph header states v14.%s, not v14.3" % (minor or "0")]
                return 0.0
            if major in ("15", "16"):
                self.last_evidence = ["official Luraph header states v%s, not v14.3" % major]
                return 0.0
            self.last_evidence = ["official Luraph header states v%s%s" % (
                major, "." + minor if minor is not None else ""
            )]
            return 0.0

        version = None
        if HEADER_ANY.search(comments):
            version = re.search(r"v?(1[3-6])\.(\d+)", comments, re.I)
            if version:
                major, minor = version.group(1), version.group(2)
                if major == "14" and minor == "3":
                    self.last_evidence = ["rebranded leading Luraph header states v14.3"]
                    return 0.96
                self.last_evidence = ["rebranded Luraph header states v%s.%s, not v14.3" % (major, minor)]
                return 0.0
            self.last_evidence = ["Luraph header found, but its version is not stated"]
            return 0.35

        if re.search(r"luraph", comments, re.I):
            version = re.search(r"v?(1[3-6])\.(\d+)", comments, re.I)
            if version:
                major, minor = version.group(1), version.group(2)
                if major == "14" and minor == "3":
                    self.last_evidence = ["Luraph named in a leading comment with version v14.3"]
                    return 0.96
                self.last_evidence = ["Luraph leading comment states v%s.%s, not v14.3" % (major, minor)]
                return 0.0
            self.last_evidence = ["unversioned Luraph mention in a leading comment"]
            return 0.25

        if _BLOB_RX.search(source):
            self.last_evidence = ["encoded Luraph blob transport found, but no versioned header"]
            return 0.3

        self.last_evidence = []
        return 0.0

    def add_arguments(self, parser):
        pass

    def deobfuscate(self, job):
        from . import driver

        out_path = job.path(".v143.recovered.lua")
        return driver.deobfuscate_file(job.source_path, out_path, job)
