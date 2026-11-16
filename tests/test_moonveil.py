import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOBF_DIR = ROOT / "deobf"
if str(DEOBF_DIR) not in sys.path:
    sys.path.insert(0, str(DEOBF_DIR))

from obfuscators import all_scores, by_name
from obfuscators.moonveil_v145 import MoonVeilV145
from obfuscators.moonveil_v211 import MoonVeilV211
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

    def test_moonveil_routes_through_unified_selector(self):
        command = bot.bot.get_command("do")
        self.assertIsNotNone(command)
        self.assertIs(command, bot.bot.get_command("deobf"))
        self.assertIn("moonveil_v145", bot.SUPPORTED)
        self.assertEqual(bot.SUPPORTED["moonveil_v145"]["command"], ".do")
        engine_options = [option.value for option in bot._EngineSelect().options]
        self.assertIn("moonveil", engine_options)
        self.assertNotIn("moonveil_v145", engine_options)
        self.assertEqual(bot.SUPPORTED["moonveil_v145"]["label"], "MoonVeil v1.4.5")


if __name__ == "__main__":
    unittest.main()


class MoonVeilV211Tests(unittest.IsolatedAsyncioTestCase):
    def test_leading_moonveil_v211_banner_is_identified_but_not_enabled(self):
        source = "-- This script was generated using MoonVeil 2.1.1 [https://moonveil.cc]\nreturn 1"
        rows = all_scores(source)
        self.assertEqual(rows[0][0], "moonveil_v211")
        self.assertEqual(rows[0][1], 1.0)
        self.assertEqual(by_name("moonveil_v211").label, "MoonVeil v2.1.1")
        self.assertNotIn("moonveil_v211", bot.SUPPORTED)

    def test_moonveil_v211_banner_inside_string_is_not_detected(self):
        source = 'local value = "MoonVeil 2.1.1"\nreturn value'
        self.assertEqual(MoonVeilV211().detect(source), 0.0)

    def test_version_picker_exposes_the_integrated_and_pending_versions(self):
        context = type("Context", (), {"author": type("Author", (), {"id": 123})()})()
        view = bot._MoonVeilVersionView(
            context,
            ("url", "https://example.com/script.lua"),
            123,
        )
        buttons = [
            item for item in view.walk_children()
            if isinstance(item, bot.discord.ui.Button)
        ]
        self.assertEqual([button.label for button in buttons], [
            "v1.4.5",
            "v2.1.1 · not ready",
        ])
        self.assertEqual(buttons[0].style, bot.discord.ButtonStyle.success)
        self.assertEqual(buttons[1].style, bot.discord.ButtonStyle.secondary)

    async def test_pending_version_button_explains_missing_engine_without_starting_job(self):
        context = type("Context", (), {"author": type("Author", (), {"id": 123})()})()
        view = bot._MoonVeilVersionView(
            context,
            ("url", "https://example.com/script.lua"),
            123,
        )
        button = next(
            item for item in view.walk_children()
            if isinstance(item, bot._MoonVeilVersionButton) and item.engine is None
        )
        interaction = type("Interaction", (), {
            "user": type("User", (), {"id": 123})(),
            "response": type("Response", (), {"edit_message": unittest.mock.AsyncMock()})(),
        })()

        await button.callback(interaction)

        interaction.response.edit_message.assert_awaited_once()
        self.assertTrue(view.claimed)
        self.assertTrue(view.is_finished())

    async def test_integrated_version_button_opens_confirmation(self):
        source = ("url", "https://example.com/script.lua")
        context = type("Context", (), {"author": type("Author", (), {"id": 123})()})()
        view = bot._MoonVeilVersionView(context, source, 123)
        button = next(
            item for item in view.walk_children()
            if isinstance(item, bot._MoonVeilVersionButton) and item.engine == "moonveil_v145"
        )
        message = type("Message", (), {})()
        interaction = type("Interaction", (), {
            "user": type("User", (), {"id": 123})(),
            "message": message,
            "response": type("Response", (), {"edit_message": unittest.mock.AsyncMock()})(),
        })()

        with unittest.mock.patch.object(bot, "_ConfirmDeobfView") as confirm:
            await button.callback(interaction)

        confirm.assert_called_once_with(
            "moonveil_v145",
            source,
            ctx=context,
            owner_id=123,
        )
        self.assertIs(confirm.return_value.message, message)
        interaction.response.edit_message.assert_awaited_once()
        self.assertTrue(view.claimed)

    async def test_version_picker_timeout_deletes_its_message(self):
        context = type("Context", (), {"author": type("Author", (), {"id": 123})()})()
        view = bot._MoonVeilVersionView(
            context,
            ("url", "https://example.com/script.lua"),
            123,
        )
        message = type("Message", (), {"delete": unittest.mock.AsyncMock()})()
        view.message = message

        await view.on_timeout()

        message.delete.assert_awaited_once_with()
        self.assertIsNone(view.message)
