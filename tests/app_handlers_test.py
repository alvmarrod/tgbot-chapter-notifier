import os
import unittest
from datetime import datetime
from unittest.mock import AsyncMock

print("Setting up test environment")
os.environ["TB_CHAPTER_NOTIFIER_TEST"] = "True"

try:
    import src.utils as icons
    import src.app.handlers as hdlrs
    from src.app.client import memory, LANG_DICT, DATABASE_FILEPATH
    from src.app.dispatcher import Responder
except ModuleNotFoundError:
    import utils as icons
    import app.handlers as hdlrs
    from app.client import memory, LANG_DICT, DATABASE_FILEPATH
    from app.dispatcher import Responder


class TestAppHandlers(unittest.IsolatedAsyncioTestCase):
    """Tests for the app handlers"""

    async def test_start(self):
        """Test the start handler"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace("roger_test", "test_start_db"))
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace("roger_test", "test_start_db"))

        mock_resp.reply_text.assert_called_once_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

    async def test_start_twice_in_same_group(self):
        """Test the start handler twice in the same group"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_start_twice_in_same_group_db"
        ))
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)
        mock_resp.reply_text.assert_called_once_with(
            LANG_DICT["cmd"]["start"]["done"]
        )

        await hdlrs.start(responder=mock_resp, chat_id=1)
        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_start_twice_in_same_group_db"
        ))

        mock_resp.reply_text.assert_called_with(
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
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.trigger_add_manga(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))

        mock_resp.send_message.assert_called_once_with(
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
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.trigger_add_manga(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_add_manga_db"
        ))

        mock_resp.send_message.assert_called_with(
            1,
            LANG_DICT["cmd"]["add"]["help"],
            reply_markup=[
                [],
                [{"text": "X", "callback_data": "tg_add_manga:X:0"}]
            ]
        )

    async def test_cb_add_manga_x(self):
        """Test the callback for trigger_add_manga handler when the user
        presses the X button"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_add_manga_x_db"
        ))
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_add_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_add_manga:X:0",
            callback_id="cb_1",
            message_id=3,
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_cb_add_manga_x_db"
        ))

        mock_resp.edit_text.assert_called_with(
            LANG_DICT["cmd"]["add"]["cancel"]
        )

    async def test_trigger_del_manga_chat_not_initialised(self):
        """Test the trigger_del_manga handler when the chat is not initialised
        """

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_not_initialised_db"
        ))
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.trigger_del_manga(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_not_initialised_db"
        ))

        mock_resp.send_message.assert_called_once_with(
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
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.trigger_del_manga(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_no_sus_db"
        ))

        mock_resp.reply_text.assert_called_with(
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_add_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_add_manga:2:0",
            callback_id="cb_1",
            message_id=1,
        )

        await hdlrs.trigger_del_manga(responder=mock_resp, chat_id=1)

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_del_manga_chat_initialised_with_sus_db"
        ))

        mock_resp.reply_text.assert_called_with(
            LANG_DICT["cmd"]["del"]["help"],
            reply_markup=[
                [{"text": "Test Manga 3",
                  "callback_data": "tg_del_manga:0:0"}],
                [{"text": "X",
                  "callback_data": "tg_del_manga:X:0"}]
            ]
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_del_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_del_manga:X:0",
            callback_id="cb_1",
            message_id=2,
        )

        mock_resp.edit_text.assert_called_with(
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_add_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_add_manga:2:0",
            callback_id="cb_1",
            message_id=1,
        )

        await hdlrs.trigger_del_manga(responder=mock_resp, chat_id=1)

        await hdlrs.cb_del_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_del_manga:0:0",
            callback_id="cb_2",
            message_id=1,
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_del_manga_complete_sequence_db"
        ))

        mock_resp.answer_callback.assert_called_with(
            LANG_DICT["cmd"]["del"]["done"]
        )
        mock_resp.edit_text.assert_called_with(
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
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.trigger_list_suscribed_mangas(
            responder=mock_resp, chat_id=1
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_not_initialised"
        ))

        mock_resp.send_message.assert_called_once_with(
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
        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.trigger_list_suscribed_mangas(
            responder=mock_resp, chat_id=1
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_no_sus"
        ))

        mock_resp.reply_text.assert_called_with(
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.trigger_list_suscribed_mangas(
            responder=mock_resp, chat_id=1
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_trigger_list_suscribed_manga_chat_initialised_with_sus"
        ))

        mock_resp.reply_text.assert_called_with(
            LANG_DICT["cmd"]["list"]["done"],
            reply_markup=[
                [
                    {"text": "Test Manga 1",
                     "callback_data": "tg_list_sc_mangas:0:0"},
                    {"text": "Test Manga 2",
                     "callback_data": "tg_list_sc_mangas:1:0"},
                    {"text": "Test Manga 3",
                     "callback_data": "tg_list_sc_mangas:2:0"},
                ],
                [{"text": "X",
                  "callback_data": "tg_list_sc_mangas:X:0"}]
            ]
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_list_suscribed_mangas(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_list_sc_mangas:X:0",
            callback_id="cb_1",
            message_id=2,
        )

        mock_resp.edit_text.assert_called_with(
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_add_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_add_manga:2:0",
            callback_id="cb_1",
            message_id=1,
        )

        await hdlrs.trigger_list_suscribed_mangas(
            responder=mock_resp, chat_id=1
        )

        await hdlrs.cb_list_suscribed_mangas(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_list_sc_mangas:0:0",
            callback_id="cb_2",
            message_id=1,
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        mock_resp.edit_text.assert_called_with(
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

        mock_resp: Responder = AsyncMock(spec=Responder)

        await hdlrs.start(responder=mock_resp, chat_id=1)

        await hdlrs.cb_add_manga(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_add_manga:2:0",
            callback_id="cb_1",
            message_id=1,
        )

        await hdlrs.trigger_list_suscribed_mangas(
            responder=mock_resp, chat_id=1
        )

        await hdlrs.cb_list_suscribed_mangas(
            responder=mock_resp,
            chat_id=1,
            callback_data="tg_list_sc_mangas:0:0",
            callback_id="cb_2",
            message_id=1,
        )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_list_manga_complete_sequence"
        ))

        mock_resp.edit_text.assert_called_with(
            LANG_DICT["cmd"]["info"]["done"] % (
                "Test Manga 3",
                icons.LAST_ICON, "Last Chapter",
                icons.CALENDAR_ICON, "2024-11-10 14:14:00",
                icons.LINK_ICON, "https://test.com/last_chapter"
            )
        )

    async def test_callback_router(self):
        """Test the assignment of the callback router via CALLBACK_MAP"""

        memory.close()
        memory.init(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_callback_router"
        ))

        memory.insert_chat(1, "Test Group")

        mock_resp: Responder = AsyncMock(spec=Responder)

        scenarios: dict[str, dict] = {
            "tg_add_manga": {
                "callback_data": "tg_add_manga:X:0",
                "chat_id": 1,
            },
            "tg_del_manga": {
                "callback_data": "tg_del_manga:0:0",
                "chat_id": 1,
            },
            "tg_list_sc_mangas": {
                "callback_data": "tg_list_sc_mangas:0:0",
                "chat_id": 1,
            },
        }

        hdlrs.CALLBACK_MAP["tg_add_manga"] = AsyncMock()
        hdlrs.CALLBACK_MAP["tg_del_manga"] = AsyncMock()
        hdlrs.CALLBACK_MAP["tg_list_sc_mangas"] = AsyncMock()

        for caller, params in scenarios.items():
            await hdlrs.CALLBACK_MAP[caller](
                responder=mock_resp,
                chat_id=params["chat_id"],
                callback_data=params["callback_data"],
                callback_id="cb_1",
                message_id=1,
            )

        memory.close()
        os.remove(DATABASE_FILEPATH.replace(
            "roger_test",
            "test_callback_router"
        ))

        for caller in scenarios:
            hdlrs.CALLBACK_MAP[caller].assert_called_once()
