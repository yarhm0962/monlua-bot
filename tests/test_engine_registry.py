import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "deobf"))

from obfuscators import PLUGINS, by_name


class NewEngineRegistryTests(unittest.TestCase):
    def test_all_three_engines_are_registered(self):
        self.assertEqual(by_name("ironveil_v1").label, "Ironveil v1")
        self.assertEqual(by_name("77fuscator").label, "77fuscator")
        self.assertEqual(by_name("ironbrew2").label, "IronBrew2")
        self.assertGreaterEqual(len(PLUGINS), 11)

    def test_ironveil_v1_banner_is_detected(self):
        engine = by_name("ironveil_v1")
        self.assertEqual(engine.detect("--[[ Obfuscated using ironveil v1 ]]\nreturn 1"), 1.0)

    def test_77fuscator_watermark_is_detected(self):
        engine = by_name("77fuscator")
        source = "do local a=[[77fuscator 0.6.1 EARLY BUILD]] end"
        self.assertEqual(engine.detect(source), 1.0)

    def test_ironbrew2_marker_is_detected(self):
        engine = by_name("ironbrew2")
        self.assertEqual(engine.detect("-- IronBrew2\nreturn function() end"), 1.0)

    def test_ironbrew1_remains_available_for_legacy_detection(self):
        self.assertEqual(by_name("ironbrew1").label, "ironbrew1")
        self.assertEqual(by_name("ironbrew2").label, "IronBrew2")

    def test_ironbrew2_is_the_only_selectable_ironbrew_engine(self):
        bot_source = (Path(__file__).resolve().parents[1] / "bot.py").read_text(encoding="utf-8")
        self.assertIn('"ironbrew2": {"label": "IronBrew2"', bot_source)
        self.assertNotIn('"ironbrew1": {"label":', bot_source)


if __name__ == "__main__":
    unittest.main()
