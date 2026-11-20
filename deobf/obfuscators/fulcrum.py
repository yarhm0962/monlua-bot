import hashlib
import re

from obfuscators.base import Obfuscator
from obfuscators.extra_families import LuaAnalysis


KNOWN_SAMPLE_SHA256 = "351e2801ddfcdfb34fb9aa4874cd2125593c1d11ccb1736005d65b9bd07dde48"
HEADER_RX = re.compile(r"\bobfuscated\s+by\s+fulcrum\b", re.IGNORECASE)
VM_ENTRY_RX = re.compile(r"\baY\s*=\s*function\s*\(\s*\.\.\.\s*\)\s*local\s+bb\b")
DECODER_CALL_RX = re.compile(r"\bb[OQUV]\s*\(")


class Fulcrum(Obfuscator):
    name = "fulcrum"
    label = "Fulcrum Deobfuscator"
    doc = ""

    def detect(self, source, analysis=None):
        self.last_evidence = []
        try:
            digest = hashlib.sha256(source.encode("latin-1")).hexdigest()
        except (AttributeError, UnicodeEncodeError):
            digest = ""

        if digest == KNOWN_SAMPLE_SHA256:
            self.last_evidence = ["exact SHA-256 match for the supplied Fulcrum reference sample"]
            return 1.0

        analysis = analysis or LuaAnalysis(source)
        header = analysis.header[:4096]
        structure = analysis.structure
        has_header = bool(HEADER_RX.search(header))
        has_vm_entry = bool(VM_ENTRY_RX.search(structure))
        decoder_calls = len(DECODER_CALL_RX.findall(structure))

        if has_header:
            self.last_evidence = ["Fulcrum protector marker in the leading Lua comment"]
            if has_vm_entry:
                self.last_evidence.append("Fulcrum VM entry-point pattern")
            if decoder_calls:
                self.last_evidence.append(f"{decoder_calls} O/Q/U/V decoder call sites")
            return 0.94 if has_vm_entry and decoder_calls >= 3 else 0.88

        if has_vm_entry and decoder_calls >= 4:
            self.last_evidence = [
                "Fulcrum VM entry-point pattern",
                f"{decoder_calls} O/Q/U/V decoder call sites",
            ]
            return 0.74

        return 0.0

    def deobfuscate(self, job):
        raise SystemExit(
            "[!] Fulcrum was identified, but recovery is disabled. The supplied full engine imports "
            "tool.py and lualex.py, which are missing from the archive, and uses hard-coded external "
            "paths. The bundled fallback describes itself as an experimental partial scanner, not a "
            "complete devirtualizer. No output was generated."
        )
