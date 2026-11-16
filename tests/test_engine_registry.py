import unittest

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


if __name__ == "__main__":
    unittest.main()
