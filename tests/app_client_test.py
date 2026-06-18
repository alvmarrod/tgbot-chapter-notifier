import os
import unittest

print("Setting up test environment")
os.environ["TB_CHAPTER_NOTIFIER_TEST"] = "True"

try:
    import src.app.client as client
    from src.infrastructure.broker import BrokerConfig
except ModuleNotFoundError:
    import app.client as client
    from infrastructure.broker import BrokerConfig


class TestAppClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the app client module"""

    def test_broker_config_from_env(self):
        """Test that the broker config loads from environment variables"""

        config: BrokerConfig = client.broker_config
        self.assertIsInstance(config, BrokerConfig)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 5672)

    def test_bot_id_loaded(self):
        """Test that BOT_ID is loaded from environment"""
        self.assertEqual(client.BOT_ID, "chaptnotifier")

    def test_subscriber_id_loaded(self):
        """Test that SUBSCRIBER_ID is loaded from environment"""
        self.assertEqual(client.SUBSCRIBER_ID, "svc_chaptnotifier")

    def test_bot_commands_list(self):
        """Test that BOT_COMMANDS contains expected commands"""
        commands = {c["command"] for c in client.BOT_COMMANDS}
        self.assertIn("start", commands)
        self.assertIn("add", commands)
        self.assertIn("del", commands)
        self.assertIn("list", commands)
