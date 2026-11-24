import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import bot
sys.path.insert(0, str(bot.DEOB_DIR))
from deobf.lexer import pretty, tokenize
from obfuscators.extra_families import LuaAnalysis


class BotPerformanceRegressionTests(unittest.IsolatedAsyncioTestCase):
    async def test_request_accepted_message_is_deleted_after_three_seconds(self):
        interaction = SimpleNamespace(delete_original_response=AsyncMock())
        with patch.object(bot.asyncio, "sleep", new=AsyncMock()) as sleep:
            await bot._delete_request_accepted_message(interaction)
        sleep.assert_awaited_once_with(3)
        interaction.delete_original_response.assert_awaited_once()
    def test_comment_stripping_preserves_strings_and_removes_comments(self):
        source = 'local a = "-- keep"\nlocal b = [=[-- keep]=]\n-- remove\n--[=[ remove block ]=]\nlocal c = "done"'
        output = bot._strip_lua_comments(source)
        self.assertIn('"-- keep"', output)
        self.assertIn("[=[-- keep]=]", output)
        self.assertIn('local c = "done"', output)
        self.assertNotIn("-- remove", output)
        self.assertNotIn("remove block", output)

    def test_comment_cleanup_handles_large_comment_dense_sources(self):
        source = "".join("-- removable comment\nlocal value = 1\n" for _ in range(5000))
        output = bot._strip_lua_comments(source)
        self.assertNotIn("-- removable comment", output)
        self.assertEqual(output.count("local value = 1"), 5000)

    def test_lexer_handles_long_bracket_comments_and_strings(self):
        source = "--[=[hidden]=]\nlocal value = [==[kept -- text]==]"
        tokens = tokenize(source)
        self.assertIn(("str", "[==[kept -- text]==]"), tokens)
        self.assertIn(("comment", "--[=[hidden]=]"), tokens)
        self.assertNotIn("hidden", pretty(tokens))

    def test_lua_analysis_reuses_correct_structural_patterns(self):
        analysis = LuaAnalysis("function run()\n for i = 1, 3 do\n if i > 0 then end\n end\nend")
        self.assertEqual(analysis.function_count, 1)
        self.assertEqual(analysis.loop_count, 1)
        self.assertEqual(analysis.branch_count, 1)

    def test_large_output_skips_the_second_formatting_pass(self):
        source = "local value = 1\n" * ((bot.MAX_FORMAT_BYTES // 16) + 2)
        self.assertGreater(len(source), bot.MAX_FORMAT_BYTES)
        self.assertEqual(bot._beautify_lua(source), source.strip())

    def test_detection_registry_lists_every_engine(self):
        self.assertEqual(len(bot.SUPPORTED), 15)
        for engine in ("ironveil_v1", "77fuscator", "ironbrew1", "ironbrew2", "luraph_v143", "luraph_v147", "luraph_v148", "luraph_v149", "luraph_v15", "luraph_v151", "moonsec_v3", "centurion", "moonveil_v145", "fulcrum", "jayfuscator"):
            self.assertIn(engine, bot.SUPPORTED)
        body = bot.engines_body()
        for label in ("IronBrew1", "IronBrew2", "Jayfuscator", "Fulcrum Deobfuscator", "v14.7", "v14.9", "v14.3", "MoonSec V3", "Centurion", "MoonVeil", "ENV LOGGER", ".l"):
            self.assertIn(label, body)
        self.assertNotIn("SERVER SETTINGS", body)

    def test_engine_commands_are_replaced_by_a_detection_notice(self):
        shortcut = bot.bot.get_command("do")
        self.assertIsNotNone(shortcut)
        self.assertIs(shortcut, bot.bot.get_command("deobf"))

    async def test_deobfuscate_command_answers_with_the_removal_notice(self):
        class Context:
            author = SimpleNamespace(id=123)

            async def reply(self, **kwargs):
                self.sent = kwargs

        ctx = Context()
        await bot.deobfuscate_command.callback(ctx)
        view = ctx.sent["view"]
        texts = [item.content for item in view.walk_children() if hasattr(item, "content")]
        self.assertTrue(any("Deobfuscation engines removed" in text for text in texts))

    def test_command_response_views_use_components_v2(self):
        self.assertIsInstance(bot.info_view("Status", "Ready"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.error_view("Error", "Failed"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.result_view("input.lua", "Engine", 128, "ok", None, "1s"), bot.discord.ui.LayoutView)
class OutputDeliveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_output_giver_prefers_rubis_then_falls_back_to_pastefy(self):
        with patch.object(bot, "_rubis_upload", return_value=("https://rubis.app/view/?scrap=abc", "https://api.rubis.app/v2/scrap/abc/raw")):
            self.assertEqual(bot._upload_output("code", "title"), ("Rubiš", "https://rubis.app/view/?scrap=abc", "https://api.rubis.app/v2/scrap/abc/raw"))
        with patch.object(bot, "_rubis_upload", return_value=("", "")), patch.object(
            bot, "_pastefy_upload", return_value="https://pastefy.app/test"
        ):
            self.assertEqual(bot._upload_output("code", "title"), ("Pastefy", "https://pastefy.app/test", "https://pastefy.app/test/raw"))
        with patch.object(bot, "_rubis_upload", return_value=("", "")), patch.object(
            bot, "_pastefy_upload", return_value=""
        ):
            self.assertEqual(bot._upload_output("code", "title"), ("", "", ""))
        self.assertEqual(bot._upload_output("", "title"), ("", "", ""))

    async def test_failed_attachment_uses_online_output_before_removing_status(self):
        class Context:
            guild = SimpleNamespace(filesize_limit=8 * 1024 * 1024)

            def __init__(self):
                self.calls = 0

            async def reply(self, **kwargs):
                self.calls += 1
                uploaded_file = kwargs.get("file")
                if uploaded_file is not None:
                    uploaded_file.close()
                if self.calls == 1:
                    raise RuntimeError("simulated Discord upload failure")
                return True

        class Status:
            def __init__(self):
                self.deleted = 0
                self.edited = []

            async def delete(self):
                self.deleted += 1

            async def edit(self, **kwargs):
                self.edited.append(kwargs)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "recovered.luau"
            output.write_text("local recovered = true\n", encoding="utf-8")
            ctx = Context()
            status = Status()
            with patch.object(bot, "_upload_output", return_value=("Pastefy", "https://pastefy.app/test", "https://pastefy.app/test/raw")):
                delivered = await bot._deliver_deobf_output(
                    ctx, status, "input.lua", "Luraph v15", output, 2000, None, "2s"
                )
        self.assertTrue(delivered)
        self.assertEqual(ctx.calls, 2)
        self.assertEqual(status.deleted, 1)
        self.assertEqual(status.edited, [])

    async def test_failed_delivery_keeps_status_and_displays_error(self):
        class Context:
            guild = SimpleNamespace(filesize_limit=1)

            async def reply(self, **kwargs):
                raise RuntimeError("unexpected attachment attempt")

        class Status:
            def __init__(self):
                self.deleted = 0
                self.edited = []

            async def delete(self):
                self.deleted += 1

            async def edit(self, **kwargs):
                self.edited.append(kwargs)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "recovered.luau"
            output.write_text("local recovered = true\n", encoding="utf-8")
            status = Status()
            with patch.object(bot, "_upload_output", return_value=("", "", "")):
                delivered = await bot._deliver_deobf_output(
                    Context(), status, "input.lua", "Luraph v15", output, 2000, None, "2s"
                )
        self.assertFalse(delivered)
        self.assertEqual(status.deleted, 0)
        self.assertEqual(len(status.edited), 1)


if __name__ == "__main__":
    unittest.main()
