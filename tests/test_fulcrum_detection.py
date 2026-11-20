import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOB_DIR = ROOT / "deobf"
if str(DEOB_DIR) not in sys.path:
    sys.path.insert(0, str(DEOB_DIR))

from obfuscators import PLUGINS, by_name
from obfuscators.extra_families import LuaAnalysis
from obfuscators.fulcrum import Fulcrum, KNOWN_SAMPLE_SHA256

import bot as bot_module


class FulcrumDetectionTests(unittest.TestCase):
    def setUp(self):
        self.engine = Fulcrum()

    def test_fulcrum_leading_header_is_detected(self):
        source = "-- Obfuscated by Fulcrum\nlocal value = 1\nreturn value"
        self.assertGreaterEqual(self.engine.detect(source), 0.88)

    def test_fulcrum_vm_shape_is_detected_without_header(self):
        source = (
            "aY = function(...) local bb = ... "
            "bO(data, key, seed) bQ(data, key, seed) "
            "bU(data, key, seed) bV(data, key, seed) return bb end"
        )
        self.assertGreaterEqual(self.engine.detect(source), 0.74)

    def test_markers_inside_strings_and_nonleading_comments_are_ignored(self):
        string_source = 'local marker = "Obfuscated by Fulcrum"\nreturn marker'
        comment_source = "local value = 1\n-- Obfuscated by Fulcrum\nreturn value"
        self.assertEqual(self.engine.detect(string_source), 0.0)
        self.assertEqual(self.engine.detect(comment_source), 0.0)

    def test_analysis_object_uses_masked_executable_structure(self):
        source = (
            "-- header without Fulcrum\n"
            'local text = "aY=function(...)local bb bO(x,y,z)"\n'
            "return text"
        )
        analysis = LuaAnalysis(source)
        self.assertEqual(self.engine.detect(source, analysis), 0.0)

    def test_reference_digest_is_the_digest_from_the_uploaded_report(self):
        report_path = ROOT / "tests" / "fixtures" / "fulcrum_reference_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(KNOWN_SAMPLE_SHA256, report["sha256"])
        self.assertTrue(report["fulcrum_header"])
        self.assertTrue(report["known_sample"])

    def test_existing_obfuscator_sample_corpora_do_not_match_fulcrum(self):
        sample_roots = [
            DEOB_DIR / "centurion" / "samples",
            DEOB_DIR / "v151" / "samples_v15.1_deobfuscated",
        ]
        sample_paths = sorted({
            path
            for root in sample_roots
            if root.is_dir()
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in {".lua", ".luau", ".txt"}
        })
        self.assertGreaterEqual(len(sample_paths), 10)
        for path in sample_paths:
            source = path.read_bytes().decode("latin-1")
            confidence = self.engine.detect(source)
            self.assertLess(
                confidence,
                0.75,
                f"Fulcrum detector falsely matched existing sample: {path.relative_to(ROOT)}",
            )

    def test_all_existing_detector_signature_samples_remain_distinct(self):
        encoded = '"' + ("x" * 80) + '"'
        params = [chr(97 + i // 26) + chr(97 + i % 26) for i in range(20)]
        cases = [
            ("luraph v15.1 vm", "return setmetatable({[75]=bit32.rrotate,[84]=table.concat}, function() end)\nlocal marker = LPH_ENCSTR\nreturn marker"),
            ("luraph v15.1 official header", "-- This file was protected using Luraph Obfuscator v15.1 [https://lura.ph/]\nreturn 1"),
            ("luraph v15.0 official header", "-- This file was protected using Luraph Obfuscator v15.0 [https://lura.ph/]\nreturn 1"),
            ("ironbrew1 wrapper", "return(function(" + ",".join(params) + ",...) local bh={1,2,3} end)"),
            ("moonsec v3 decoder", "\n".join("r(1," + encoded + ")" for _ in range(6))),
            ("centurion factory", "local c3 = {}\n" + "\n".join("c3[%d] = function(Z) return Z end" % index for index in range(1, 22))),
            ("synapse xen identifiers", "\n".join("local SynapseXen_signal_%d = true" % index for index in range(18))),
            ("jayfuscator transport", "-- Jayfuscator V1.2.1\nlocal bi = Dc(\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\")\nreturn bj(bv(bg()), {}, bg())()"),
            ("ironveil header", "-- Obfuscated using ironveil v1\nreturn 1"),
            ("77fuscator marker", "do local a=[[77fuscator 0.6.1 EARLY BUILD]] end"),
            ("ironbrew2 header", "-- IronBrew2\nreturn function() end"),
        ]
        for label, source in cases:
            self.assertLess(
                self.engine.detect(source),
                0.75,
                f"Fulcrum detector misclassified the existing {label} fixture",
            )

    def test_reference_luraph_report_is_not_a_fulcrum_match(self):
        report_path = ROOT / "tests" / "fixtures" / "fulcrum_luraph_reference_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertFalse(report["fulcrum_header"])
        self.assertFalse(report["known_sample"])
        self.assertNotEqual(report["sha256"], KNOWN_SAMPLE_SHA256)

    def test_plugin_is_registered(self):
        self.assertTrue(any(plugin.name == "fulcrum" for plugin in PLUGINS))
        self.assertEqual(by_name("fulcrum").label, "Fulcrum Deobfuscator")

    def test_unavailable_engine_detection_is_reported_for_jayfuscator_only(self):
        match = bot_module._unavailable_engine_match([
            ("jayfuscator", 0.94, "jayfuscator", ["header matched"]),
        ])
        self.assertEqual(match, ("jayfuscator", 0.94))
        # Fulcrum recovery is live now, so even a confident hit is never "unavailable"
        self.assertIsNone(bot_module._unavailable_engine_match([
            ("fulcrum", 0.94, "Fulcrum Deobfuscator", ["header matched"]),
        ]))
        self.assertIsNone(bot_module._unavailable_engine_match([
            ("fulcrum", 0.74, "Fulcrum Deobfuscator", ["shape only"]),
        ]))

    def test_bot_enables_recovery_with_the_full_engine(self):
        self.assertIn("fulcrum", bot_module.SUPPORTED)
        self.assertTrue(bot_module._engine_is_available("fulcrum"))
        self.assertTrue(any(option.value == "fulcrum" for option in bot_module._engine_select_options()))
        context = type("Context", (), {"author": type("Author", (), {"id": 123})()})()
        view = bot_module._EnginePickerView(context, ("url", "https://example.com/sample.lua"))
        unavailable = [
            item for item in view.walk_children()
            if isinstance(item, bot_module.discord.ui.Button)
            and "Fulcrum Deobfuscator" in item.label
        ]
        # Fulcrum is pickable in the engine select, so it must not appear as an
        # "unavailable" button anymore
        self.assertEqual(len(unavailable), 0)

    def test_deobfuscation_fails_closed_without_emitting_output(self):
        import os
        import tempfile
        work = tempfile.mkdtemp(prefix="fulcrum_plugin_")
        src = os.path.join(work, "plain.lua")
        with open(src, "w", encoding="utf-8") as f:
            f.write('print("hello world")\n')
        args = type("Args", (), {"timeout": 120})()

        class Job:
            pass
        job = Job()
        job.source_path = src
        job.args = args
        job.trace_path = os.path.join(work, "plain.deobf.luau")
        job.outdir = os.path.join(work, "output")
        try:
            with self.assertRaises(RuntimeError) as raised:
                self.engine.deobfuscate(job)
            self.assertIn("fulcrum engine failed", str(raised.exception))
        finally:
            self.assertFalse(os.path.exists(os.path.join(job.outdir, "fulcrum_deobfuscated.lua")),
                             "a failed run must not leave an output file")


if __name__ == "__main__":
    unittest.main()
