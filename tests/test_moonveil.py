import sys
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOBF_DIR = ROOT / "deobf"
if str(DEOBF_DIR) not in sys.path:
    sys.path.insert(0, str(DEOBF_DIR))

from obfuscators import all_scores, by_name
from obfuscators.moonveil_v145 import MoonVeilV145
from obfuscators.moonveil_v211 import MoonVeilV211
import bot


class MoonVeilDetectionTests(unittest.TestCase):
    def test_leading_moonveil_v145_banner_is_detected(self):
        source = "-- MoonVeil Obfuscator v1.4.5\nlocal value = 1\nreturn value"
        rows = all_scores(source)
        self.assertEqual(rows[0][0], "moonveil_v145")
        self.assertEqual(rows[0][1], 1.0)
        self.assertEqual(by_name("moonveil_v145").label, "MoonVeil v1.4.5")

    def test_moonveil_banner_inside_string_is_not_detected(self):
        source = 'local value = "MoonVeil Obfuscator v1.4.5"\nreturn value'
        self.assertEqual(MoonVeilV145().detect(source), 0.0)


    def test_leading_moonveil_v211_banner_is_identified_but_not_enabled(self):
        source = "-- This script was generated using MoonVeil 2.1.1 [https://moonveil.cc]\nreturn 1"
        rows = all_scores(source)
        self.assertEqual(rows[0][0], "moonveil_v211")
        self.assertEqual(rows[0][1], 1.0)
        self.assertEqual(by_name("moonveil_v211").label, "MoonVeil v2.1.1")
        self.assertNotIn("moonveil_v211", bot.SUPPORTED)

    def test_moonveil_v211_banner_inside_string_is_not_detected(self):
        source = 'local value = "MoonVeil 2.1.1"\nreturn value'
        self.assertEqual(MoonVeilV211().detect(source), 0.0)

