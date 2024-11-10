import os
import unittest
from datetime import datetime
from pyrogram.client import Client
from pyrogram.enums import ChatType
from pyrogram.types import (
    Message,
    Chat,
    User,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from unittest.mock import AsyncMock
from typing import Callable, Awaitable

print("Setting up test environment")
os.environ["TB_CHAPTER_NOTIFIER_TEST"] = "True"

try:
    import src.utils as icons
    import src.app.handlers as hdlrs
    from src.app.client import memory, LANG_DICT, DATABASE_FILEPATH
except ModuleNotFoundError:
    import utils as icons
    import app.handlers as hdlrs
    from app.client import memory, LANG_DICT, DATABASE_FILEPATH


class TestAppHandlers(unittest.IsolatedAsyncioTestCase):
    """Tests for the app handlers"""

    async def test_start(self):
        """Test the start handler"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace("roger_test", "test_start_db"))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        # We mock the reply_text function from the message object, so can check
        mock_msg.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace("roger_test", "test_start_db"))

        mock_msg.reply_text.assert_called_once_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

    async def test_start_twice_in_same_group(self):
        """Test the start handler twice in the same group"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_start_twice_in_same_group_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        # We mock the reply_text function from the message object, so can check
        mock_msg.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg)
        mock_msg.reply_text.assert_called_once_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.start(mock_clt, mock_msg)
        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_start_twice_in_same_group_db"
        ))

        mock_msg.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["error"]
        )

    async def test_trigger_add_manga_chat_not_initialised(self):
        """Test the trigger_add_manga handler when the chat is not initialised
        """

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_clt.send_message = AsyncMock()

        await hdlrs.trigger_add_manga(mock_clt, mock_msg)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))

        mock_clt.send_message.assert_called_once_with(
            1,
            LANG_DICT["generic"]["notStarted"]
        )

    async def test_trigger_add_manga_chat_initialised(self):
        """Test the trigger_add_manga handler when the chat is initialised"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_add: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        # We mock the reply_text function from the message object, so can check
        mock_msg_start.reply_text = AsyncMock()
        mock_clt.send_message = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.trigger_add_manga(mock_clt, mock_msg_add)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))

        mock_clt.send_message.assert_called_with(
            1,
            LANG_DICT["cmd"]["add"]["help"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_add_manga:X:0')]]
            )
        )

    async def test_cb_add_manga_x(self):
        """Test the callback for trigger_add_manga handler when the user
        presses the X button"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_add_manga_x_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_add: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_x: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_add_manga:X:0",
            message=Message(
                id=3,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        # We mock the reply_text function from the message object, so can check
        mock_msg_start.reply_text = AsyncMock()
        mock_clt.send_message = AsyncMock()
        mock_msg_x.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.trigger_add_manga(mock_clt, mock_msg_add)

        mock_clt.send_message.assert_called_with(
            1,
            LANG_DICT["cmd"]["add"]["help"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_add_manga:X:0')]]
            )
        )

        await hdlrs.cb_add_manga(mock_clt, mock_msg_x)

        mock_msg_x.message.edit_text.assert_called_with(
            LANG_DICT["cmd"]["add"]["cancel"]
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_add_manga_x_db"
        ))

    async def test_trigger_del_manga_chat_not_initialised(self):
        """Test the trigger_del_manga handler when the chat is not initialised
        """

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_not_initialised_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        # We mock the reply_text function from the message object, so can check
        mock_clt.send_message = AsyncMock()

        await hdlrs.trigger_del_manga(mock_clt, mock_msg)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_not_initialised_db"
        ))

        mock_clt.send_message.assert_called_once_with(
            1,
            LANG_DICT["generic"]["notStarted"]
        )

    async def test_trigger_del_manga_chat_initialised_no_sus(self):
        """Test the trigger_del_manga handler when the chat is initialised,
        but there are no suscriptions"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_no_sus_db"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_del: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        # We mock the reply_text function from the message object, so can check
        mock_msg_start.reply_text = AsyncMock()
        mock_msg_del.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.trigger_del_manga(mock_clt, mock_msg_del)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_no_sus_db"
        ))

        mock_msg_del.reply_text.assert_called_with(
            LANG_DICT["cmd"]["del"]["empty"]
        )

    async def test_trigger_del_manga_chat_initialised_with_sus(self):
        """Test the trigger_del_manga handler when the chat is initialised,
        when there is at least 1 suscription"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_with_sus_db"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_add: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_add_manga:2:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_del: Message = Message(
            id=3,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_cb_add.answer = AsyncMock()
        mock_cb_add.message.edit_text = AsyncMock()
        mock_msg_del.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_add_manga(mock_clt, mock_cb_add)

        mock_cb_add.answer.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["done"]
        )
        mock_cb_add.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["selection"] % "Test Manga 3"
        )

        await hdlrs.trigger_del_manga(mock_clt, mock_msg_del)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_with_sus_db"
        ))

        mock_msg_del.reply_text.assert_called_with(
            LANG_DICT["cmd"]["del"]["help"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Test Manga 3',
                        callback_data='tg_del_manga:0:0')],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_del_manga:X:0')]
                ]
            )
        )

    async def test_cb_del_manga_x(self):
        """Test the callback for trigger_del_manga handler when the user
        presses the X button"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_del_manga_x_db"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        self.assertTrue(memory.insert_suscription(1, "Test Manga 1", ""))

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_del_x: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_del_manga:X:0",
            message=Message(
                id=2,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_clt.send_message = AsyncMock()
        mock_cb_del_x.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_del_manga(mock_clt, mock_cb_del_x)

        mock_cb_del_x.message.edit_text.assert_called_with(
            LANG_DICT["cmd"]["del"]["cancel"]
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_del_manga_x_db"
        ))

    async def test_del_manga_complete_sequence(self):
        """Test the full sequence of the del_manga handler"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_del_manga_complete_sequence_db"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_add: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_add_manga:2:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_del: Message = Message(
            id=3,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_del: CallbackQuery = CallbackQuery(
            id="2",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_del_manga:0:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_cb_add.answer = AsyncMock()
        mock_cb_add.message.edit_text = AsyncMock()
        mock_msg_del.reply_text = AsyncMock()
        mock_cb_del.answer = AsyncMock()
        mock_cb_del.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_add_manga(mock_clt, mock_cb_add)

        mock_cb_add.answer.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["done"]
        )
        mock_cb_add.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["selection"] % "Test Manga 3"
        )

        await hdlrs.trigger_del_manga(mock_clt, mock_msg_del)

        mock_msg_del.reply_text.assert_called_with(
            LANG_DICT["cmd"]["del"]["help"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Test Manga 3',
                        callback_data='tg_del_manga:0:0'
                    )],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_del_manga:X:0')]
                ]
            )
        )

        await hdlrs.cb_del_manga(mock_clt, mock_cb_del)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_del_manga_complete_sequence_db"
        ))

        mock_cb_del.answer.assert_called_once_with(
            LANG_DICT["cmd"]["del"]["done"]
        )

        mock_cb_del.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["del"]["selection"] % "Test Manga 3"
        )

    async def test_trigger_list_suscribed_manga_chat_not_initialised(self):
        """Test the trigger_list_suscribed_mangas handler when the chat
        is not initialised"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_not_initialised"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_clt.send_message = AsyncMock()

        await hdlrs.trigger_list_suscribed_mangas(mock_clt, mock_msg)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_not_initialised"
        ))

        mock_clt.send_message.assert_called_once_with(
            1,
            LANG_DICT["generic"]["notStarted"]
        )

    async def test_trigger_list_suscribed_manga_chat_initialised_no_sus(self):
        """Test the trigger_list_suscribed_mangas handler when the chat
        is initialised, but there are no suscriptions"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_no_sus"
        ))
        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_list: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_msg_list.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.trigger_list_suscribed_mangas(mock_clt, mock_msg_list)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_no_sus"
        ))

        mock_msg_list.reply_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["empty"]
        )

    async def test_trigger_list_suscribed_manga_chat_initialised_with_sus(self):
        """Test the trigger_list_suscribed_mangas handler when the chat
        is initialised, and there are suscriptions"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_with_sus"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        self.assertTrue(memory.insert_suscription(1, "Test Manga 1", ""))
        self.assertTrue(memory.insert_suscription(1, "Test Manga 2", ""))
        self.assertTrue(memory.insert_suscription(1, "Test Manga 3", ""))

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_list: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_msg_list.reply_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.trigger_list_suscribed_mangas(mock_clt, mock_msg_list)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_with_sus"
        ))

        mock_msg_list.reply_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["done"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Test Manga 1',
                        callback_data='tg_list_sc_mangas:0:0'),
                    InlineKeyboardButton(
                        text='Test Manga 2',
                        callback_data='tg_list_sc_mangas:1:0'),
                    InlineKeyboardButton(
                        text='Test Manga 3',
                        callback_data='tg_list_sc_mangas:2:0')],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_list_sc_mangas:X:0')]
                ]
            )
        )

    async def test_cb_list_suscribed_manga_x(self):
        """Test the callback for trigger_list_suscribed_mangas handler when the
        user presses the X button"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_list_suscribed_manga_x"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        self.assertTrue(memory.insert_suscription(1, "Test Manga 1", ""))
        self.assertTrue(memory.insert_suscription(1, "Test Manga 2", ""))
        self.assertTrue(memory.insert_suscription(1, "Test Manga 3", ""))

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_list_x: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_list_sc_mangas:X:0",
            message=Message(
                id=2,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_clt.send_message = AsyncMock()
        mock_cb_list_x.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_list_suscribed_mangas(mock_clt, mock_cb_list_x)

        mock_cb_list_x.message.edit_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["cancel"]
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_list_suscribed_manga_x"
        ))

    async def test_list_manga_complete_sequence_last_not_available(self):
        """Test the full sequence of the list_manga handler when the manga
        last chapter is not available"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_add: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_add_manga:2:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_list: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_list: CallbackQuery = CallbackQuery(
            id="2",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_list_sc_mangas:0:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_cb_add.answer = AsyncMock()
        mock_cb_add.message.edit_text = AsyncMock()
        mock_msg_list.reply_text = AsyncMock()
        mock_cb_list.answer = AsyncMock()
        mock_cb_list.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_add_manga(mock_clt, mock_cb_add)

        mock_cb_add.answer.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["done"]
        )
        mock_cb_add.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["selection"] % "Test Manga 3"
        )

        await hdlrs.trigger_list_suscribed_mangas(mock_clt, mock_msg_list)

        mock_msg_list.reply_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["done"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Test Manga 3',
                        callback_data='tg_list_sc_mangas:0:0')],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_list_sc_mangas:X:0')]
                ]
            )
        )

        await hdlrs.cb_list_suscribed_mangas(mock_clt, mock_cb_list)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        mock_cb_list.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["info"]["lastNotAvailable"] % "Test Manga 3"
        )

    async def test_list_manga_complete_sequence_last_available(self):
        """Test the full sequence of the list_manga handler when the manga
        last chapter is available"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        memory.insert_manga("Test Manga 1", "https://test.com")
        memory.insert_manga("Test Manga 2", "https://test.com")
        memory.insert_manga("Test Manga 3", "https://test.com")

        memory.insert_manga_chapter(
            "Last Chapter",
            "Last Chapter",
            "https://test.com/last_chapter",
            datetime.strptime("2024-11-10 14:14", "%Y-%m-%d %H:%M"),
            "Test Manga 3",
        )

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        mock_msg_start: Message = Message(
            id=1,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_add: CallbackQuery = CallbackQuery(
            id="1",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_add_manga:2:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_list: Message = Message(
            id=2,
            chat=Chat(
                id=1,
                type=ChatType.PRIVATE,
                title="Test Group"
            ),
        )

        mock_cb_list: CallbackQuery = CallbackQuery(
            id="2",
            from_user=User(id=1),
            chat_instance="1",
            data="tg_list_sc_mangas:0:0",
            message=Message(
                id=1,
                chat=Chat(
                    id=1,
                    type=ChatType.PRIVATE,
                    title="Test Group"
                )
            )
        )

        mock_msg_start.reply_text = AsyncMock()
        mock_cb_add.answer = AsyncMock()
        mock_cb_add.message.edit_text = AsyncMock()
        mock_msg_list.reply_text = AsyncMock()
        mock_cb_list.answer = AsyncMock()
        mock_cb_list.message.edit_text = AsyncMock()

        await hdlrs.start(mock_clt, mock_msg_start)
        mock_msg_start.reply_text.assert_called_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.cb_add_manga(mock_clt, mock_cb_add)

        mock_cb_add.answer.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["done"]
        )
        mock_cb_add.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["add"]["selection"] % "Test Manga 3"
        )

        await hdlrs.trigger_list_suscribed_mangas(mock_clt, mock_msg_list)

        mock_msg_list.reply_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["done"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Test Manga 3',
                        callback_data='tg_list_sc_mangas:0:0')],
                    [InlineKeyboardButton(
                        text='X',
                        callback_data='tg_list_sc_mangas:X:0')]
                ]
            )
        )

        await hdlrs.cb_list_suscribed_mangas(mock_clt, mock_cb_list)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        mock_cb_list.message.edit_text.assert_called_once_with(
            LANG_DICT["cmd"]["info"]["done"] % (
                "Test Manga 3",
                icons.LAST_ICON, "Last Chapter",
                icons.CALENDAR_ICON, "2024-11-10 14:14:00",
                icons.LINK_ICON, "https://test.com/last_chapter"
            )
        )

    async def test_callback_router(self):
        """Test the assignment of the callback router.
        We will assume the callback is just """

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_callback_router"
        ))

        memory.insert_chat(1, "Test Group")

        mock_clt: Client = Client(name="Chapter Notifier Bot")

        scenarios: dict[str, CallbackQuery] = {
            "tg_add_manga": CallbackQuery(
                id="1",
                from_user=User(id=1),
                chat_instance="1",
                data="tg_add_manga:X:0",
                message=Message(
                    id=1,
                    chat=Chat(
                        id=1,
                        type=ChatType.PRIVATE,
                        title="Test Group"
                    )
                )
            ),
            "tg_del_manga": CallbackQuery(
                id="2",
                from_user=User(id=1),
                chat_instance="1",
                data="tg_del_manga:0:0",
                message=Message(
                    id=1,
                    chat=Chat(
                        id=1,
                        type=ChatType.PRIVATE,
                        title="Test Group"
                    )
                )
            ),
            "tg_list_sc_mangas": CallbackQuery(
                id="3",
                from_user=User(id=1),
                chat_instance="1",
                data="tg_list_sc_mangas:0:0",
                message=Message(
                    id=1,
                    chat=Chat(
                        id=1,
                        type=ChatType.PRIVATE,
                        title="Test Group"
                    )
                )
            ),
            "mistaken": CallbackQuery(
                id="4",
                from_user=User(id=1),
                chat_instance="1",
                data="mistaken:0:0",
                message=Message(
                    id=1,
                    chat=Chat(
                        id=1,
                        type=ChatType.PRIVATE,
                        title="Test Group"
                    )
                )
            )
        }

        mock_clt.send_message = AsyncMock()

        hdlrs.CALLBACK_MAP["tg_add_manga"] = AsyncMock()
        hdlrs.CALLBACK_MAP["tg_del_manga"] = AsyncMock()
        hdlrs.CALLBACK_MAP["tg_list_sc_mangas"] = AsyncMock()

        for scenario in scenarios:
            await hdlrs.callback_router(mock_clt, scenarios[scenario])

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_callback_router"
        ))

        hdlrs.CALLBACK_MAP["tg_add_manga"].assert_called_once_with(
            mock_clt,
            scenarios["tg_add_manga"]
        )
        hdlrs.CALLBACK_MAP["tg_del_manga"].assert_called_once_with(
            mock_clt,
            scenarios["tg_del_manga"]
        )
        hdlrs.CALLBACK_MAP["tg_list_sc_mangas"].assert_called_once_with(
            mock_clt,
            scenarios["tg_list_sc_mangas"]
        )

        mock_clt.send_message.assert_called_with(
            1,
            LANG_DICT["generic"]["error"]
        )
