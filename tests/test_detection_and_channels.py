import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOB_DIR = ROOT / "deobf"
if str(DEOB_DIR) not in sys.path:
    sys.path.insert(0, str(DEOB_DIR))

from obfuscators import all_scores
from obfuscators.extra_families import (
    leading_lua_comments,
    scan_lua_source,
    strip_lua_comments,
)
from obfuscators.ironbrew1 import Ironbrew1
from obfuscators.luraph_v151 import LuraphV151
from obfuscators.moonsec_v3 import MoonsecV3

import bot as bot_module


class LuaDetectionTests(unittest.TestCase):
    def test_comment_scanner_does_not_strip_comment_text_inside_strings(self):
        source = (
            '-- ordinary header comment\n'
            'local quoted = "-- this is string data"\n'
            'local bracketed = [=[-- also string data]=]\n'
            '--[=[ a long comment\ncontinued here ]=]\n'
            'return quoted, bracketed\n'
        )
        code, comments = scan_lua_source(source)
        self.assertIn('"-- this is string data"', code)
        self.assertIn('[=[-- also string data]=]', code)
        self.assertNotIn("ordinary header comment", code)
        self.assertIn("continued here", comments)
        self.assertEqual(leading_lua_comments(source).splitlines()[0], "-- ordinary header comment")

    def test_commentless_luraph_is_detected_from_vm_shape(self):
        source = (
            "return setmetatable({[75]=bit32.rrotate,"
            "LPH_ENCSTR=function() end}, function() end)"
        )
        result = LuraphV151().detect(source)
        self.assertGreaterEqual(result, 0.80)

    def test_commentless_ironbrew_is_detected_from_wrapper_shape(self):
        params = [chr(97 + i // 26) + chr(97 + i % 26) for i in range(20)]
        source = "return(function(" + ",".join(params) + ",...) local bh={1,2,3} end)"
        self.assertGreaterEqual(Ironbrew1().detect(source), 0.80)

    def test_commentless_moonsec_is_detected_from_decoder_calls(self):
        encoded = '"' + ("x" * 80) + '"'
        source = "\n".join("r(1," + encoded + ")" for _ in range(6))
        self.assertGreaterEqual(MoonsecV3().detect(source), 0.75)

    def test_family_candidates_are_ranked_with_supported_engines(self):
        source = "\n".join("local SynapseXen_signal_%d = true" % i for i in range(18))
        rows = all_scores(source)
        self.assertEqual(rows[0][0], "xen")
        self.assertGreaterEqual(rows[0][1], 0.85)

    def test_brand_names_inside_strings_are_not_treated_as_header_comments(self):
        source = 'local x = "This file was protected with MoonSec V3"\nreturn x'
        self.assertEqual(MoonsecV3().detect(source), 0.0)


class ChannelCommandTests(unittest.TestCase):
    def test_required_slash_commands_are_registered(self):
        roots = {command.name: command for command in bot_module.bot.tree.get_commands()}
        self.assertIn("set", roots)
        self.assertIn("remove", roots)
        set_channel = roots["set"].get_command("channel")
        remove_set = roots["remove"].get_command("set")
        self.assertIsNotNone(set_channel)
        self.assertIsNotNone(remove_set)
        remove_channel = remove_set.get_command("channel")
        self.assertIsNotNone(remove_channel)
        self.assertTrue(next(p for p in set_channel.parameters if p.name == "channel").required)
        self.assertTrue(next(p for p in remove_channel.parameters if p.name == "channel").required)

    def test_channel_policy_is_per_server_and_strict_when_configured(self):
        original = {key: list(value) for key, value in bot_module.CHANNEL_RESTRICTIONS.items()}
        try:
            bot_module.CHANNEL_RESTRICTIONS.clear()
            self.assertTrue(bot_module._channel_is_allowed(101, 202))
            bot_module.CHANNEL_RESTRICTIONS["101"] = [202, 203]
            self.assertTrue(bot_module._channel_is_allowed(101, 202))
            self.assertFalse(bot_module._channel_is_allowed(101, 204))
            self.assertTrue(bot_module._channel_is_allowed(303, 404))
        finally:
            bot_module.CHANNEL_RESTRICTIONS.clear()
            bot_module.CHANNEL_RESTRICTIONS.update(original)


if __name__ == "__main__":
    unittest.main()
