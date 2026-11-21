"""Regression tests for the durable /set channel allowlist.

The service filesystem is wiped by every deploy and restart, so the channel
settings are mirrored into the private jobs repo and re-applied on boot. These
tests exercise that round-trip against a fake GitHub contents API.
"""

import asyncio
import base64
import json
import unittest
from unittest.mock import patch

import bot as bot_module

CONFIG_PATH = "config/channel_restrictions.json"


class _FakeGitHub:
    """Minimal in-memory contents API for the endpoints the bot touches."""

    def __init__(self, existing=None):
        self.store = dict(existing or {})
        self.sha = "seed-sha-1"

    def __call__(self, method, path, *, body=None, accept="application/vnd.github+json"):
        key = (method, path.split("?")[0])
        if method == "GET":
            if key not in self.store:
                return 404, b"not found"
            payload = {"content": base64.b64encode(self.store[key]).decode("ascii"), "sha": self.sha}
            return 200, json.dumps(payload).encode("utf-8")
        if method == "PUT":
            if "sha" in (body or {}) and body["sha"] != self.sha:
                return 409, b"conflict"
            self.store[key] = base64.b64decode(body["content"])
            self.sha = "seed-sha-2"
            return 200, json.dumps({"content": {"sha": self.sha}}).encode("utf-8")
        raise AssertionError(f"unexpected method {method}")

    def stored(self):
        return self.store.get(("PUT", f"/repos/{bot_module.GH_JOBS_REPO}/contents/{CONFIG_PATH}"))


class ChannelRemoteConfigTests(unittest.TestCase):
    def setUp(self):
        bot_module._channel_config_remote_sha = None
        bot_module._channel_config_restored = False
        self._old_restrictions = dict(bot_module.CHANNEL_RESTRICTIONS)

    def tearDown(self):
        bot_module.CHANNEL_RESTRICTIONS.clear()
        bot_module.CHANNEL_RESTRICTIONS.update(self._old_restrictions)
        bot_module._channel_config_remote_sha = None
        bot_module._channel_config_restored = False

    def test_push_creates_remote_config_when_absent(self):
        fake = _FakeGitHub()
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            ok = asyncio.run(bot_module._push_channel_restrictions_remote({"111": [222]}))
        self.assertTrue(ok)
        self.assertEqual(json.loads(fake.stored()), {"111": [222]})

    def test_push_updates_existing_remote_config(self):
        existing = json.dumps({"111": [222]}).encode("utf-8")
        fake = _FakeGitHub({("GET", f"/repos/{bot_module.GH_JOBS_REPO}/contents/{CONFIG_PATH}"): existing})
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            ok = asyncio.run(bot_module._push_channel_restrictions_remote({"111": [222, 333]}))
        self.assertTrue(ok)
        self.assertEqual(json.loads(fake.stored()), {"111": [222, 333]})

    def test_push_recovers_from_stale_blob_sha(self):
        existing = json.dumps({"111": [222]}).encode("utf-8")
        fake = _FakeGitHub({("GET", f"/repos/{bot_module.GH_JOBS_REPO}/contents/{CONFIG_PATH}"): existing})
        bot_module._channel_config_remote_sha = "definitely-stale"
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            ok = asyncio.run(bot_module._push_channel_restrictions_remote({"111": [222]}))
        self.assertTrue(ok)
        self.assertEqual(json.loads(fake.stored()), {"111": [222]})

    def test_fetch_rejects_corrupt_remote_payload(self):
        fake = _FakeGitHub({("GET", f"/repos/{bot_module.GH_JOBS_REPO}/contents/{CONFIG_PATH}"): b"{not json"})
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            remote, sha = asyncio.run(asyncio.to_thread(bot_module._fetch_remote_channel_state))
        self.assertIsNone(remote)
        self.assertIsNone(sha)

    def test_push_without_cloud_token_is_noop(self):
        fake = _FakeGitHub()
        with patch.object(bot_module, "cloud_runner_configured", return_value=False), \
             patch.object(bot_module, "_gh_api", fake):
            ok = asyncio.run(bot_module._push_channel_restrictions_remote({"111": [222]}))
        self.assertFalse(ok)
        self.assertIsNone(fake.stored())

    def test_restore_applies_remote_config_to_memory(self):
        existing = json.dumps({"1558873751645585449": [1571227168644534404]}).encode("utf-8")
        fake = _FakeGitHub({("GET", f"/repos/{bot_module.GH_JOBS_REPO}/contents/{CONFIG_PATH}"): existing})
        bot_module.CHANNEL_RESTRICTIONS.clear()
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            asyncio.run(bot_module._restore_channel_restrictions_remote())
        self.assertEqual(
            dict(bot_module.CHANNEL_RESTRICTIONS), {"1558873751645585449": [1571227168644534404]}
        )

    def test_restore_without_remote_keeps_memory_and_backs_it_up(self):
        fake = _FakeGitHub()
        bot_module.CHANNEL_RESTRICTIONS.clear()
        bot_module.CHANNEL_RESTRICTIONS["111"] = [222]
        with patch.object(bot_module, "cloud_runner_configured", return_value=True), \
             patch.object(bot_module, "_gh_api", fake):
            asyncio.run(bot_module._restore_channel_restrictions_remote())
        self.assertEqual(dict(bot_module.CHANNEL_RESTRICTIONS), {"111": [222]})
        self.assertEqual(json.loads(fake.stored()), {"111": [222]})


if __name__ == "__main__":
    unittest.main()
