import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOB_DIR = ROOT / "deobf"
if str(DEOB_DIR) not in sys.path:
    sys.path.insert(0, str(DEOB_DIR))

from obfuscators.fulcrum import (
    Fulcrum,
    KNOWN_FULCRUM_SAMPLE_SHA256,
    KNOWN_LURAPH_CONTROL_SHA256,
    is_known_fulcrum_sample_digest,
    sample_digest,
)


class FulcrumReferenceSampleTests(unittest.TestCase):
    def test_archived_positive_reports_share_the_known_fulcrum_fingerprint(self):
        reports = (
            ("fulcrum_direct_test.json", KNOWN_FULCRUM_SAMPLE_SHA256, True),
            ("fulcrum_heuristic_test.json", KNOWN_FULCRUM_SAMPLE_SHA256, True),
            ("test_report.json", KNOWN_FULCRUM_SAMPLE_SHA256, True),
        )
        for name, digest, expected in reports:
            with self.subTest(report=name):
                self.assertEqual(is_known_fulcrum_sample_digest(digest), expected)

    def test_archived_luraph_control_reports_are_not_fulcrum(self):
        reports = (
            ("fulcrum_luraph_direct_test.json", KNOWN_LURAPH_CONTROL_SHA256, False),
            ("test_luraph_report.json", KNOWN_LURAPH_CONTROL_SHA256, False),
        )
        for name, digest, expected in reports:
            with self.subTest(report=name):
                self.assertEqual(is_known_fulcrum_sample_digest(digest), expected)

    def test_exact_digest_matches_raw_byte_hashing(self):
        payload = b"local payload = 42"
        self.assertEqual(sample_digest(payload), sample_digest(payload.decode("latin-1")))

    def test_header_requires_corroborating_vm_shape(self):
        engine = Fulcrum()
        header_only = "-- Obfuscated by Fulcrum\nreturn 1"
        self.assertEqual(engine.detect(header_only), 0.0)

        source = (
            "-- Obfuscated by Fulcrum\n"
            "v1 = {}; v2(v1); "
            "bO(data, key, seed); bQ(data, key, seed); bU(data, key, seed)"
        )
        self.assertGreaterEqual(engine.detect(source), 0.95)

    def test_brand_text_inside_a_string_is_not_a_header(self):
        engine = Fulcrum()
        source = 'local text = "Obfuscated by Fulcrum"; return text'
        self.assertEqual(engine.detect(source), 0.0)

    def test_archive_luraph_control_is_excluded(self):
        engine = Fulcrum()
        self.assertEqual(engine.detect("control"), 0.0)
        self.assertFalse(is_known_fulcrum_sample_digest(KNOWN_LURAPH_CONTROL_SHA256))

    def test_incomplete_engine_does_not_return_unverified_output(self):
        engine = Fulcrum()
        with self.assertRaisesRegex(RuntimeError, "recovery is disabled"):
            engine.deobfuscate(None)


if __name__ == "__main__":
    unittest.main()
