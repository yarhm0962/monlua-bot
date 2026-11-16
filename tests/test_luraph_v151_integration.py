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
        ready, detail = bot.runtime_status("luraph_v151")
        self.assertTrue(ready, detail)

    def test_pinned_upstream_runtime_metadata_is_configured(self):
        self.assertEqual(bot.V151_UPSTREAM_COMMIT, "337d9563202559c092a7a9618c4ac284aceae385")
        self.assertEqual(set(bot.V151_RUNTIME_FILES), {"luau", "luau-ast", "luau.exe", "luau-ast.exe"})
        for name in ("luau", "luau-ast"):
            size, blob_sha = bot.V151_RUNTIME_FILES[name]
            self.assertGreater(size, 0)
            self.assertEqual(len(blob_sha), 40)


if __name__ == "__main__":
    unittest.main()
