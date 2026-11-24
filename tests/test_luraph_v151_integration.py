import json
import os
import subprocess
import unittest

import bot


class LuraphV151IntegrationTests(unittest.TestCase):
    def test_luraph_v151_is_registered_for_detection(self):
        self.assertIn("luraph_v151", bot.SUPPORTED)
        self.assertEqual(bot.SUPPORTED["luraph_v151"]["label"], "Luraph v15.1")

    def test_v151_header_scores_full_confidence(self):
        source = "-- This file was protected using Luraph Obfuscator v15.1 [https://lura.ph/]\nreturn 1"
        plugin = __import__("sys").modules.get("obfuscators")
        if plugin is None:
            import sys as _sys
            _sys.path.insert(0, str(bot.DEOB_DIR))
            plugin = _sys.modules.setdefault("obfuscators", __import__("obfuscators"))
        rows = [(plugin.by_name("luraph_v151").detect(source),)]
        self.assertEqual(rows[0][0], 1.0)

    def test_bot_still_registers_the_do_and_detect_commands(self):
        self.assertIsNotNone(bot.bot.get_command("do"))
        self.assertIsNotNone(bot.bot.get_command("detect"))


if __name__ == "__main__":
    unittest.main()
