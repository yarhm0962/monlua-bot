import os
import re
import sys
from pathlib import Path

from obfuscators.base import Obfuscator

DEOBF_ROOT = Path(__file__).resolve().parents[2]
HEADER = re.compile(r"MoonVeil(?:\s+Obfuscator)?\s+v?1\.4\.5\b", re.IGNORECASE)


class MoonVeilV145(Obfuscator):
    name = "moonveil_v145"
    label = "MoonVeil v1.4.5"
    doc = "MOONVEIL.md"

    def detect(self, source, analysis=None):
        if analysis is None:
            from obfuscators.extra_families import LuaAnalysis
            analysis = LuaAnalysis(source)
        if HEADER.search(analysis.header[:4000]):
            self.last_evidence = ["MoonVeil v1.4.5 version banner in leading comments"]
            return 1.0
        self.last_evidence = []
        return 0.0

    def deobfuscate(self, job):
        try:
            from moonveil.core import find_luau
            from moonveil.v145_pipeline import recover_v145
        except Exception as exc:
            raise RuntimeError("MoonVeil v1.4.5 package could not be imported: %s" % exc) from exc

        configured = os.environ.get("LUAU_PATH")
        local_runtime = DEOBF_ROOT / "bin" / ("luau.exe" if os.name == "nt" else "luau")
        if configured:
            luau_path = find_luau(None, DEOBF_ROOT)
        elif local_runtime.is_file():
            luau_path = local_runtime
        else:
            luau_path = find_luau(None, DEOBF_ROOT)

        if os.name != "nt" and not os.access(luau_path, os.X_OK):
            raise RuntimeError("MoonVeil Luau runtime is not executable: %s" % luau_path)

        timeout = float(getattr(job.args, "timeout", 0) or 300)
        timeout = max(30.0, min(1800.0, timeout - 15.0))
        result = recover_v145(
            Path(job.source_path),
            luau_path=luau_path,
            timeout=timeout,
            verify=True,
        )
        recovered_source = result.recovered_source.strip()
        if not recovered_source:
            raise RuntimeError("MoonVeil returned an empty recovery result")

        destination = job.path("_moonveil_result.luau")
        job.write(destination, recovered_source + "\n")

        verification = result.verification or {}
        if verification.get("equivalent") is True:
            print(
                "[+] MoonVeil: sandbox behavior verification matched %s events"
                % verification.get("original_event_count", 0),
                file=sys.stderr,
            )
        elif verification.get("compiled") is True:
            print("[+] MoonVeil: recovered Luau passed compiler validation", file=sys.stderr)
        else:
            print("[!] MoonVeil: recovery completed but compiler/behavior verification was inconclusive", file=sys.stderr)

        for note in result.notes:
            print("[!] MoonVeil: " + str(note), file=sys.stderr)

        return destination
