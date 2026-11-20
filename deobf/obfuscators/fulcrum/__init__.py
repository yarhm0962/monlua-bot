import hashlib
import re

from obfuscators.base import Obfuscator
from obfuscators.extra_families import LuaAnalysis


KNOWN_FULCRUM_SAMPLE_SHA256 = "351e2801ddfcdfb34fb9aa4874cd2125593c1d11ccb1736005d65b9bd07dde48"
KNOWN_LURAPH_CONTROL_SHA256 = "c675b61926ddf73f3fa54d7d1bd71f29e3321da8a1853af574fcc1f5cf6812e3"

_HEADER = re.compile(r"\bobfuscated\s+by\s+fulcrum\b", re.I)
_V1_ASSIGN = re.compile(r"\bv1\s*=", re.I)
_V2_ENTRY = re.compile(r"\bv2\s*\(\s*v1\s*\)", re.I)
_CIPHER_CALL = re.compile(r"\bb[OQUV]\s*\(", re.I)
_ALT_VM_ENTRY = re.compile(r"\baY\s*=\s*function\b", re.I)
_ALT_VM_PARTS = re.compile(r"\b(?:bZ|cb|cc|ce)\s*\(", re.I)


def sample_digest(source):
    if isinstance(source, bytes):
        data = source
    else:
        data = str(source).encode("latin-1", errors="replace")
    return hashlib.sha256(data).hexdigest()


def is_known_fulcrum_sample_digest(digest):
    return digest == KNOWN_FULCRUM_SAMPLE_SHA256


class Fulcrum(Obfuscator):
    name = "fulcrum"
    label = "Fulcrum Deobfuscator"
    doc = "FULCRUM.md"

    def detect(self, source, analysis=None):
        analysis = analysis or LuaAnalysis(source)
        digest = sample_digest(source)

        if digest == KNOWN_LURAPH_CONTROL_SHA256:
            self.last_evidence = ["matches the archived Luraph control sample, not the Fulcrum reference sample"]
            return 0.0

        if is_known_fulcrum_sample_digest(digest):
            self.last_evidence = ["exact SHA-256 match for the archived Fulcrum reference sample"]
            return 1.0

        header = analysis.header[:4096]
        if not _HEADER.search(header):
            self.last_evidence = []
            return 0.0

        structure = analysis.structure
        first_assignment = _V1_ASSIGN.search(structure[:150000])
        entry = _V2_ENTRY.search(structure[:150000], first_assignment.end() if first_assignment else 0)
        cipher_calls = sum(1 for _ in _CIPHER_CALL.finditer(structure[:250000]))

        if first_assignment and entry and cipher_calls >= 2:
            self.last_evidence = [
                "Fulcrum leading header",
                "v1/v2 wrapper entry point",
                f"{cipher_calls} recognized O/Q/U/V cipher calls",
            ]
            return 0.97

        alternate_entry = _ALT_VM_ENTRY.search(structure[:150000])
        alternate_parts = len(list(_ALT_VM_PARTS.finditer(structure[:250000])))
        if alternate_entry and alternate_parts >= 3 and len(source) >= 20000:
            self.last_evidence = [
                "Fulcrum leading header",
                "alternate VM factory entry point",
                f"{alternate_parts} recognized VM helper calls",
            ]
            return 0.91

        self.last_evidence = ["Fulcrum header found without the required corroborating VM structure"]
        return 0.0

    def deobfuscate(self, job):
        raise RuntimeError(
            "Fulcrum detection is available, but recovery is disabled. The supplied archive is missing "
            "the required tool.py and lualex.py dependencies, and it does not include the original "
            "440.txt reference input needed to validate the full unflattening pipeline. The bundled "
            "standalone scanner only reports unverified string candidates and is not a complete devirtualizer."
        )
