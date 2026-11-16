import os
import unittest

import bot


class LuraphV151IntegrationTests(unittest.TestCase):
    def test_new_runner_and_runtime_paths_exist(self):
        self.assertTrue(bot.V151_SCRIPT.is_file())
        self.assertTrue(bot.V151_NODE_ARCHIVE.is_file())
        luau = bot.V151_DIR / "bin" / "luau"
        luau_ast = bot.V151_DIR / "bin" / "luau-ast"
        self.assertTrue(luau.is_file())
        self.assertTrue(luau_ast.is_file())
        self.assertTrue(os.access(luau, os.X_OK))
        self.assertTrue(os.access(luau_ast, os.X_OK))

    def test_luraph_v151_routes_through_unified_selector(self):
        command = bot.bot.get_command("do")
        self.assertIsNotNone(command)
        self.assertIs(command, bot.bot.get_command("deobf"))
        self.assertIn("luraph_v151", bot.SUPPORTED)
        self.assertEqual(bot.SUPPORTED["luraph_v151"]["command"], ".do")
        self.assertIn("luraph_v151", [option.value for option in bot._EngineSelect().options])

    def test_all_native_runtime_checks_include_luraph_binaries(self):
        ready, detail = bot.runtime_status("luraph_v151")
        self.assertTrue(ready, detail)

    def test_portable_runtime_builder_is_included(self):
        self.assertTrue((bot.V151_DIR / "build_luau.py").is_file())
        self.assertTrue((bot.V151_DIR / "INTEGRATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
