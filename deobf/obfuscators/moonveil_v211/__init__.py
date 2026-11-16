import re

from obfuscators.base import Obfuscator


HEADER = re.compile(r"MoonVeil(?:\\s+Obfuscator)?\\s+v?2\\.1\\.1\\b", re.IGNORECASE)


class MoonVeilV211(Obfuscator):
    name = "moonveil_v211"
    label = "MoonVeil v2.1.1"
    doc = ""

    def detect(self, source, analysis=None):
        if analysis is None:
            from obfuscators.extra_families import LuaAnalysis
            analysis = LuaAnalysis(source)
        if HEADER.search(analysis.header[:4000]):
            self.last_evidence = ["MoonVeil v2.1.1 version banner in leading comments"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        raise RuntimeError(
            "MoonVeil v2.1.1 is recognized, but no compatible full deobfuscation "
            "engine is installed. The supplied archive contains sample inputs "
            "only, not the v2.1.1 engine."
        )
