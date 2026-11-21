"""Luraph v14.8: pinned entry on the vendored LuraphOpenSource engine.

Shares the bundled Node/Python devirtualizer with the internal luraph_all
catch-all; detection is pinned to the Luraph v14.8 header family so the
engine list shows the real version name instead of a generic label.
"""
from obfuscators.luraph_all import LuraphAll, header_version


class LuraphV148(LuraphAll):
    name = "luraph_v148"
    label = "Luraph v14.8"
    doc = "LURAPH.md"
    engine_title = "Luraph v14.8"

    def detect(self, source, analysis=None):
        from obfuscators.extra_families import LuaAnalysis

        analysis = analysis or LuaAnalysis(source)
        version = header_version(source, analysis)
        if version and version[0] == "14" and version[1] == 8:
            self.last_evidence = ["Luraph v14.8 header; the dedicated v14.8 engine handles it natively"]
            return 1.0
        self.last_evidence = []
        return 0.0
