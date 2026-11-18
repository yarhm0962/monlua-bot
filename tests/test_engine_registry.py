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

    def test_ironbrew_versions_are_distinct_registered_engines(self):
        self.assertEqual(by_name("ironbrew1").label, "IronBrew1")
        self.assertEqual(by_name("ironbrew2").label, "IronBrew2")
        self.assertEqual(by_name("ironbrew1").detect("-- this file was generated using ironbrew1\\nreturn 1"), 1.0)
        self.assertEqual(by_name("ironbrew2").detect("-- IronBrew2\\nreturn function() end"), 1.0)

    def test_both_ironbrew_versions_are_selectable(self):
        bot_source = (Path(__file__).resolve().parents[1] / "bot.py").read_text(encoding="utf-8")
        self.assertIn('"ironbrew1": {"label": "IronBrew1"', bot_source)
        self.assertIn('"ironbrew2": {"label": "IronBrew2"', bot_source)
        self.assertIn('"ironbrew1", "ironbrew2"', bot_source)


if __name__ == "__main__":
    unittest.main()


class EngineAvailabilityTests(unittest.TestCase):
    def test_jayfuscator_is_registered_but_disabled_until_validated(self):
        import bot as bot_module

        self.assertIn("jayfuscator", bot_module.SUPPORTED)
        self.assertFalse(bot_module._engine_is_available("jayfuscator"))
        option = next(option for option in bot_module._engine_select_options() if option.value == "jayfuscator")
        self.assertTrue(option.disabled)
        self.assertIn("unavailable", option.label.lower())

    def test_unavailable_engines_are_not_recommended(self):
        import bot as bot_module

        self.assertIsNone(bot_module._recommended_engine([
            ("jayfuscator", 0.99, "Jayfuscator", ["signature matched"])
        ]))
