import os
import unittest
from pyrogram.client import Client
from unittest.mock import AsyncMock
from pyrogram.types import BotCommand

print("Setting up test environment")
os.environ["TB_CHAPTER_NOTIFIER_TEST"] = "True"

try:
    import src.app.client as client
except ModuleNotFoundError:
    import app.client as client


class TestAppClient(unittest.IsolatedAsyncioTestCase):
    """Tests for the app client module"""

    async def test_get_authorized_client(self):
        """Test that the client is created correctly"""

        my_client: Client = client._get_authorized_client()
        self.assertIsInstance(my_client, Client)
        self.assertNotEqual(my_client.api_id, 0)
        self.assertNotEqual(my_client.api_hash, "")
        self.assertNotEqual(my_client.bot_token, "")
        self.assertEqual(my_client.test_mode, False)

    async def test_set_commands_ok(self):
        """Test that the bot commands are set correctly"""

        client.pyrogram_client.set_bot_commands = AsyncMock()

        await client.set_commands()

        client.pyrogram_client.set_bot_commands.assert_called_once_with(
            [
                BotCommand(
                    command=cmd["command"],  # type: ignore
                    description=cmd["description"]  # type: ignore
                ) for cmd in client.BOT_COMMANDS
            ]
        )
