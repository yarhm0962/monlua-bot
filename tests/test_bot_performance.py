import unittest

import bot
from deobf.lexer import tokenize
from obfuscators.extra_families import LuaAnalysis


class BotPerformanceRegressionTests(unittest.TestCase):
    def test_comment_stripping_preserves_strings_and_removes_comments(self):
        source = 'local a = "-- keep"\nlocal b = [=[-- keep]=]\n-- remove\n--[=[ remove block ]=]\nlocal c = "done"'
        output = bot._strip_lua_comments(source)
        self.assertIn('"-- keep"', output)
        self.assertIn("[=[-- keep]=]", output)
        self.assertIn('local c = "done"', output)
        self.assertNotIn("-- remove", output)
        self.assertNotIn("remove block", output)

    def test_lexer_handles_long_bracket_comments_and_strings(self):
        source = "--[=[hidden]=]\nlocal value = [==[kept -- text]==]"
        tokens = tokenize(source)
        self.assertIn(("str", "[==[kept -- text]==]"), tokens)
        self.assertFalse(any(kind == "comment" and "hidden" in value for kind, value in tokens))

    def test_lua_analysis_reuses_correct_structural_patterns(self):
        analysis = LuaAnalysis("function run()\n for i = 1, 3 do\n if i > 0 then end\n end\nend")
        self.assertEqual(analysis.function_count, 1)
        self.assertEqual(analysis.loop_count, 1)
        self.assertEqual(analysis.branch_count, 1)

    def test_large_output_skips_the_second_formatting_pass(self):
        source = "local value = 1\n" * ((bot.MAX_FORMAT_BYTES // 16) + 2)
        self.assertGreater(len(source), bot.MAX_FORMAT_BYTES)
        self.assertEqual(bot._beautify_lua(source), source.strip())

    def test_command_response_views_use_components_v2(self):
        self.assertIsInstance(bot.info_view("Status", "Ready"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.error_view("Error", "Failed"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.result_view("input.lua", "Engine", 128, "ok", None, "1s"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot._ConfirmDeobfView("luraph_v15", ("url", "https://example.com")), bot.discord.ui.LayoutView)


if __name__ == "__main__":
    unittest.main()
