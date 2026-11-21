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

    def test_unified_commands_and_all_engine_options_are_registered(self):
        shortcut = bot.bot.get_command("do")
        self.assertIsNotNone(shortcut)
        self.assertIs(shortcut, bot.bot.get_command("deobf"))
        self.assertEqual(len(bot.SUPPORTED), 11)
        self.assertIn("ironveil_v1", bot.SUPPORTED)
        self.assertIn("77fuscator", bot.SUPPORTED)
        self.assertIn("ironbrew1", bot.SUPPORTED)
        self.assertIn("ironbrew2", bot.SUPPORTED)
        expected_engine_options = set(bot.SUPPORTED)
        expected_engine_options.discard("moonveil_v145")
        expected_engine_options.discard("jayfuscator")
        expected_engine_options.add("moonveil")
        self.assertEqual(
            set(option.value for option in bot._EngineSelect().options),
            expected_engine_options,
        )
        self.assertIn("IronBrew1", bot.engines_body())
        self.assertIn("IronBrew2", bot.engines_body())
        self.assertIn("Jayfuscator", bot.engines_body())
        self.assertIn("Fulcrum Deobfuscator", bot.engines_body())
        self.assertNotIn("SERVER SETTINGS", bot.engines_body())
        for engine in bot.SUPPORTED:
            self.assertEqual(bot.SUPPORTED[engine]["command"], ".do")

    def test_recommended_engine_is_selected_from_confident_supported_matches(self):
        rows = [
            ("ironbrew1", 0.81, "IronBrew1", ["header"]),
            ("ironbrew2", 0.98, "IronBrew2", ["version marker"]),
            ("obfuscated", 1.0, "Obfuscated", []),
        ]
        self.assertEqual(bot._recommended_engine(rows), "ironbrew2")
        self.assertIsNone(bot._recommended_engine([("ironbrew1", 0.74, "IronBrew1", [])]))

    def test_recommended_engine_is_first_and_both_ironbrew_versions_are_listed(self):
        options = bot._engine_select_options("ironbrew2")
        self.assertEqual(options[0].value, "ironbrew2")
        self.assertEqual(options[0].label, "IronBrew2 (Recommended)")
        self.assertIn("ironbrew1", {option.value for option in options})
        self.assertIn("ironbrew2", {option.value for option in options})

    async def test_scanned_source_bytes_are_reused_after_engine_selection(self):
        payload = b"-- IronBrew2\\nreturn function() end"

        class Attachment:
            filename = "sample.lua"
            size = len(payload)

            async def save(self, path):
                Path(path).write_bytes(payload)

        class Status:
            view = None

            async def edit(self, **kwargs):
                self.view = kwargs["view"]

        class Context:
            author = SimpleNamespace(id=123)
            message = SimpleNamespace(attachments=[Attachment()])

            async def reply(self, **kwargs):
                return status

        status = Status()
        rows = [("ironbrew2", 0.99, "IronBrew2", ["version marker"])]
        ctx = Context()
        with patch.object(bot, "_detect_scores", new=AsyncMock(return_value=(rows, "test scan"))) as scanner:
            await bot.deobfuscate_command.callback(ctx)
        scanner.assert_awaited_once()
        self.assertIsInstance(status.view, bot._EnginePickerView)
        self.assertEqual(status.view.recommended_engine, "ironbrew2")
        selector = next(item for item in status.view.walk_children() if isinstance(item, bot.discord.ui.Select))
        self.assertEqual(selector.options[0].label, "IronBrew2 (Recommended)")
        self.assertEqual(bot._source_preset(status.view.source), ("sample.lua", payload))

    def test_detect_invoker_exposes_guild_file_limit(self):
        guild = SimpleNamespace(filesize_limit=123456)
        invoker = bot._DetectInvoker(SimpleNamespace(guild=guild), owner_id=42)
        self.assertIs(invoker.guild, guild)
        self.assertEqual(invoker.author.id, 42)

    def test_confirmation_view_contains_single_use_controls(self):
        view = bot._ConfirmDeobfView("luraph_v15", ("url", "https://example.com/test.lua"), owner_id=42)
        self.assertFalse(view.claimed)
        controls = [item.custom_id for item in view.walk_children() if isinstance(item, bot.discord.ui.Button)]
        self.assertEqual(set(controls), {"deobf_confirm", "deobf_cancel"})

    def test_command_response_views_use_components_v2(self):
        self.assertIsInstance(bot.info_view("Status", "Ready"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.error_view("Error", "Failed"), bot.discord.ui.LayoutView)
        self.assertIsInstance(bot.result_view("input.lua", "Engine", 128, "ok", None, "1s"), bot.discord.ui.LayoutView)


class OutputDeliveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_output_giver_prefers_rubis_then_falls_back_to_pastefy(self):
        with patch.object(bot, "_rubis_upload", return_value=("https://rubis.app/view/?scrap=abc", "https://api.rubis.app/v2/scrap/abc/raw")):
            self.assertEqual(bot._upload_output("code", "title"), ("Rubis", "https://rubis.app/view/?scrap=abc", "https://api.rubis.app/v2/scrap/abc/raw"))
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
