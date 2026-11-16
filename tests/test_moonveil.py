import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOBF_DIR = ROOT / "deobf"
if str(DEOBF_DIR) not in sys.path:
    sys.path.insert(0, str(DEOBF_DIR))

from obfuscators import all_scores, by_name
from obfuscators.moonveil_v145 import MoonVeilV145
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

    def test_mv_command_is_registered(self):
        command = bot.bot.get_command("mv")
        self.assertIsNotNone(command)
        self.assertEqual(command.name, "mv")

    def test_supported_engine_routes_to_mv(self):
        self.assertEqual(bot.SUPPORTED["moonveil_v145"]["command"], ".mv")
        self.assertEqual(bot.SUPPORTED["moonveil_v145"]["label"], "MoonVeil v1.4.5")


if __name__ == "__main__":
    unittest.main()
