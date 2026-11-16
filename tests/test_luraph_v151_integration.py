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

    def test_luraph_v151_command_remains_registered(self):
        command = bot.bot.get_command("lrph15.1")
        self.assertIsNotNone(command)
        self.assertEqual(bot.SUPPORTED["luraph_v151"]["command"], ".lrph15.1")

    def test_all_native_runtime_checks_include_luraph_binaries(self):
        ready, detail = bot.runtime_status()
        self.assertTrue(ready, detail)


if __name__ == "__main__":
    unittest.main()
