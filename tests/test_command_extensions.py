import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import bot


class CommandExtensionRegistrationTests(unittest.TestCase):
    def test_detect_shortcut_is_registered(self):
        self.assertIs(bot.bot.get_command("detect"), bot.bot.get_command("d"))

    def test_beautify_shortcut_is_registered(self):
        self.assertIsNotNone(bot.bot.get_command("beautify"))
        self.assertIs(bot.bot.get_command("beautify"), bot.bot.get_command("b"))


class ConfirmationExpiryTests(unittest.IsolatedAsyncioTestCase):
    async def test_confirmation_timeout_deletes_original_message(self):
        view = bot._ConfirmDeobfView(
            "luraph_v15",
            ("url", "https://example.com/script.lua"),
            owner_id=123,
        )
        message = SimpleNamespace(delete=AsyncMock())
        view.message = message

        await view.on_timeout()

        message.delete.assert_awaited_once_with()
        self.assertIsNone(view.message)

    async def test_engine_picker_timeout_deletes_original_message(self):
        context = SimpleNamespace(author=SimpleNamespace(id=123))
        view = bot._EnginePickerView(context, ("url", "https://example.com/script.lua"))
        message = SimpleNamespace(delete=AsyncMock())
        view.message = message

        await view.on_timeout()

        message.delete.assert_awaited_once_with()
        self.assertIsNone(view.message)


class GetLoaderRegressionTests(unittest.TestCase):
    def test_loadstring_scanner_ignores_comments_and_string_contents(self):
        source = (
            '-- loadstring(game:HttpGet("https://ignored.example/comment.lua"))()' + "\n"
            'local text = "loadstring(game:HttpGet(https://ignored.example/string.lua))"' + "\n"
            'loadstring(game:HttpGetAsync("https://example.com/payload.lua"))()'
        )

        self.assertEqual(
            bot._extract_loadstring_url(source),
            "https://example.com/payload.lua",
        )

    def test_loadstring_scanner_reads_long_bracket_urls(self):
        source = 'loadstring(game:HttpGet([[https://example.com/long.lua]]))()'

        self.assertEqual(
            bot._extract_loadstring_url(source),
            "https://example.com/long.lua",
        )

    def test_loader_depth_only_counts_successfully_fetched_children(self):
        parent_url = "https://example.com/loader.lua"
        child_url = "https://example.com/child.lua"
        parent_body = f'loadstring(game:HttpGet("{child_url}"))()'.encode()

        def fake_validate(url, allow_any_ext=False):
            return url, "loader.lua"

        def fake_download(url, destination, allow_any_ext=False):
            if url != parent_url:
                raise ValueError("the child source is unavailable")
            destination.write_bytes(parent_body)
            return "loader.lua", len(parent_body)

        with bot.tempfile.TemporaryDirectory(prefix="get_depth_test_") as directory:
            destination = bot.Path(directory) / "result.lua"
            with patch.object(bot, "_validate_public_url", side_effect=fake_validate), patch.object(
                bot, "_download_url", side_effect=fake_download
            ):
                filename, size, depth, note = bot._download_get_source(parent_url, destination)

            self.assertEqual(filename, "loader.lua")
            self.assertEqual(destination.read_bytes(), parent_body)
            self.assertEqual(size, len(parent_body))
            self.assertEqual(depth, 0)
            self.assertIn("child source is unavailable", note)


class BeautifyPipelineTests(unittest.TestCase):
    def test_unwraps_lua_code_fences(self):
        fence = chr(96) * 3
        source = fence + "lua\nlocal value=1\n" + fence

        self.assertEqual(bot._unwrap_lua_code_block(source), "local value=1")

    def test_beautify_runs_stylua_with_verification(self):
        process_result = SimpleNamespace(
            returncode=0,
            stdout="local value = 1\n",
            stderr="",
        )
        with patch.object(bot, "_resolve_stylua", return_value="/usr/bin/stylua"), patch.object(
            bot.subprocess, "run", return_value=process_result
        ) as run:
            output = bot._beautify_source("local value=1", "script.lua")

        self.assertEqual(output, "local value = 1\n")
        args, kwargs = run.call_args
        self.assertIn("--verify", args[0])
        self.assertIn("--stdin-filepath", args[0])
        self.assertEqual(kwargs["input"], "local value=1")
        self.assertEqual(kwargs["timeout"], 30)

    def test_rejects_invalid_lua_instead_of_returning_unformatted_input(self):
        process_result = SimpleNamespace(
            returncode=2,
            stdout="",
            stderr="parse error",
        )
        with patch.object(bot, "_resolve_stylua", return_value="/usr/bin/stylua"), patch.object(
            bot.subprocess, "run", return_value=process_result
        ):
            with self.assertRaisesRegex(ValueError, "could not be parsed"):
                bot._beautify_source("local value =", "script.lua")

    def test_refuses_to_claim_success_without_a_formatter(self):
        with patch.object(bot, "_resolve_stylua", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "StyLua 2.6.0 is unavailable"):
                bot._beautify_source("local value=1", "script.lua")

    def test_small_result_is_sent_as_a_normal_discord_message(self):
        class Context:
            def __init__(self):
                self.sent = []

            async def reply(self, **kwargs):
                self.sent.append(kwargs)

            async def send(self, **kwargs):
                self.sent.append(kwargs)

        async def run_test():
            context = Context()
            await bot._send_beautified_output(context, "script.lua", "local value = 1\n")
            self.assertEqual(len(context.sent), 1)
            message = context.sent[0]
            self.assertIn("Beautified Lua", message["content"])
            self.assertIn("lua", message["content"])
            self.assertNotIn("view", message)
            self.assertNotIn("file", message)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
