from typing import Optional, Callable, Awaitable
from pyrogram.types import Message, CallbackQuery
from pyrogram.client import Client
from pyrogram import filters

try:
    from src.utils import log
    import src.utils as icons
    from src.app.client import pyrogram_client, memory, LANG_DICT
    from src.domain.model import (Manga, search_manga_by_name)
    import src.domain.communications as comms
    from src.app.messages import (
        pg_text_inline_keyboard,
        pg_get_element_by_position
    )
except ModuleNotFoundError:
    from utils import log
    import utils as icons
    from app.client import pyrogram_client, memory, LANG_DICT
    from domain.model import (Manga, search_manga_by_name)
    import domain.communications as comms
    from app.messages import (
        pg_text_inline_keyboard,
        pg_get_element_by_position
    )


###############################################################################
#                                    HANDLERS                                 #
###############################################################################

# TODO: search for patterns and extract shared logic to functions


@pyrogram_client.on_message(filters.command(["start"]))
async def start(client: Client, message: Message):
    """Start the bot for the given chat"""

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(message.chat.id)

        if not chat:
            memory.insert_chat(message.chat.id, message.chat.title)
            await message.reply_text(LANG_DICT["cmd"]["start"]["done"])

        else:
            await message.reply_text(LANG_DICT["cmd"]["start"]["error"])

    except Exception as e:
        log("bot", "error", ["start", f"Start command failed: {str(e)}"])
        await message.reply_text(LANG_DICT["generic"]["error"])


@pyrogram_client.on_message(filters.command(["add"]))
async def trigger_add_manga(client: Client, message: Message):
    """Add a manga to the list of suscribed mangas"""
    me: str = "tg_add_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(message.chat.id)

        if chat is None:
            await client.send_message(message.chat.id,
                                      LANG_DICT["generic"]["notStarted"])

        else:
            page_num: int = 0
            items: list[str] = [manga.name for manga in memory.read_mangas()]

            await client.send_message(
                message.chat.id,
                LANG_DICT["cmd"]["add"]["help"],
                reply_markup=pg_text_inline_keyboard(
                    me,
                    items,
                    3,
                    page_num
                )
            )

    except Exception as e:
        log("bot", "error",
            ["trigger_add_manga", f"Add command failed: {str(e)}"])
        await message.reply_text(LANG_DICT["generic"]["error"])


async def cb_add_manga(client: Client, callback_query: CallbackQuery):
    """Completes the logic for adding a manga to the list of suscribed mangas
    """
    me: str = "tg_add_manga"
    chat_id: int = callback_query.message.chat.id

    try:
        # After trigger, we are sure that the chat exists
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_query.data).split(":")[-1])
        selection: str = str(callback_query.data).split(":")[1]

        if selection not in ['<', '>', 'X']:

            mangas: list[str] = [manga.name for manga in memory.read_mangas()]

            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

            # Manga comes from the database, so should exists
            sel_manga: Optional[Manga] = search_manga_by_name(
                memory.read_mangas(),
                selection_name
            )
            assert sel_manga is not None, f"Manga not found: {selection_name}"

            already_exists: bool = False

            my_sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            if comms.search_suscriptions_by_manga(my_sus, sel_manga):
                already_exists = True

            if already_exists:
                await callback_query.message.edit_text(
                    (LANG_DICT["cmd"]["add"]["error"] % selection_name)
                )
                raise Exception("Suscription for this manga already exists")

            if memory.insert_suscription(
                chat_id=chat.id,
                manga_name=sel_manga.name,
                last_chapter=""
            ):
                await callback_query.answer(LANG_DICT["cmd"]["add"]["done"])
                await callback_query.message.edit_text(
                    (LANG_DICT["cmd"]["add"]["selection"] % selection_name)
                )
                log(
                    "bot", "info",
                    [
                        "cb_add_manga",
                        f"Added manga '{selection_name}' to chat '{chat.id}'"
                    ]
                )

            else:
                await callback_query.answer(
                    LANG_DICT["cmd"]["add"]["error"] % selection_name)
                log(
                    "bot", "warn",
                    [
                        "cb_add_manga",
                        f"Couldn't add manga '{selection_name}' to chat "
                        f"'{chat.id}'"
                    ]
                )

        elif selection in ['<', '>']:
            items: list[str] = [manga.name for manga in memory.read_mangas()]

            if selection == "<":
                page_num -= 1
            elif selection == ">":
                page_num += 1

            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["add"]["help"],
                reply_markup=pg_text_inline_keyboard(
                    me,
                    items,
                    3,
                    page_num
                )
            )

        elif selection == "X":
            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["add"]["cancel"]
            )

        else:
            await callback_query.answer(LANG_DICT["cmd"]["add"]["error"])

    except Exception as e:
        log("bot", "error", [
            "cb_add_manga",
            f"Add command callback failed: {str(e)}"
        ])
        await callback_query.answer(LANG_DICT["generic"]["error"])


@pyrogram_client.on_message(filters.command(["del"]))
async def trigger_del_manga(client: Client, message: Message):
    """Remove a manga from the list of suscribed mangas"""
    me: str = "tg_del_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(message.chat.id)

        if chat is None:
            await client.send_message(message.chat.id,
                                      LANG_DICT["generic"]["notStarted"])

        else:
            sus: list[comms.Suscription] = memory.read_suscription_by_chat(
                message.chat.id
            )

            if len(sus) == 0:
                await message.reply_text(LANG_DICT["cmd"]["del"]["empty"])

            else:
                items: list[str] = [sc.manga.name for sc in sus]

                await message.reply_text(
                    LANG_DICT["cmd"]["del"]["help"],
                    reply_markup=pg_text_inline_keyboard(
                        me,
                        items,
                        3,
                        0
                    )
                )

    except Exception as e:
        log("bot", "error", ["cb_del_manga", f"Del command failed: {str(e)}"])
        await message.reply_text(LANG_DICT["generic"]["error"])


async def cb_del_manga(client: Client, callback_query: CallbackQuery):
    """Completes the logic for removing a manga from the list of
    suscribed mangas for a chat
    """
    me: str = "tg_del_manga"
    chat_id: int = callback_query.message.chat.id

    try:
        # After trigger, we are sure that the chat exists
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_query.data).split(":")[-1])
        selection: str = str(callback_query.data).split(":")[1]

        if selection not in ['<', '>', 'X']:

            my_sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            mangas: list[str] = [sc.manga.name for sc in my_sus]

            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

            target_sus: Optional[comms.Suscription] = \
                next((sc for sc in my_sus if sc.manga.name == selection_name),
                     None)

            if target_sus is not None and \
                    memory.delete_suscription(target_sus.chat.id,
                                              target_sus.manga.name):
                await callback_query.answer(LANG_DICT["cmd"]["del"]["done"])
                await callback_query.message.edit_text(
                    (LANG_DICT["cmd"]["del"]["selection"] % selection_name)
                )
                log(
                    "bot", "info",
                    [
                        "cb_del_manga",
                        f"Deleted manga {selection_name} from chat {chat.id}"
                    ]
                )

            else:
                await callback_query.answer(LANG_DICT["cmd"]["del"]["error"])
                log(
                    "bot", "warn",
                    [
                        "cb_del_manga",
                        f"Couldn't delete manga {selection_name} from chat "
                        f"{chat.id}"
                    ]
                )

        elif selection in ['<', '>']:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)
            items: list[str] = [sc.manga.name for sc in sus]

            if selection == "<":
                page_num -= 1
            elif selection == ">":
                page_num += 1

            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["del"]["help"],
                reply_markup=pg_text_inline_keyboard(
                    me,
                    items,
                    3,
                    page_num
                )
            )

        elif selection == "X":
            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["del"]["cancel"]
            )

        else:
            await callback_query.answer(LANG_DICT["cmd"]["del"]["error"])

    except Exception as e:
        log("bot", "error", [
            "cb_del_manga",
            f"Del command callback failed: {str(e)}"
        ])
        await callback_query.answer(LANG_DICT["generic"]["error"])


@pyrogram_client.on_message(filters.command(["list"]))
async def trigger_list_suscribed_mangas(client: Client, message: Message):
    """List the mangas suscribed in the chat"""
    me: str = "tg_list_sc_mangas"
    chat_id: int = message.chat.id

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)

        if chat is None:
            await client.send_message(chat_id,
                                      LANG_DICT["generic"]["notStarted"])

        else:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            if len(sus) == 0:
                await message.reply_text(LANG_DICT["cmd"]["list"]["empty"])

            else:
                await message.reply_text(
                    LANG_DICT["cmd"]["list"]["done"],
                    reply_markup=pg_text_inline_keyboard(
                        me,
                        [sc.manga.name for sc in sus],
                        3,
                        0
                    )
                )

    except Exception as e:
        log("bot", "error", ["list_mangas", f"List command failed: {str(e)}"])
        await message.reply_text(LANG_DICT["generic"]["error"])


async def cb_list_suscribed_mangas(client: Client,
                                   callback_query: CallbackQuery):
    """Completes the logic for listing the mangas suscribed in the chat"""
    me: str = "tg_list_sc_mangas"
    chat_id: int = callback_query.message.chat.id

    try:
        # After trigger, we are sure that the chat exists
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_query.data).split(":")[-1])
        selection: str = str(callback_query.data).split(":")[1]

        if selection not in ['<', '>', 'X']:

            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            mangas: list[str] = [sc.manga.name for sc in sus]
            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

            # Manga comes from the database, so should exists
            sel_manga: Optional[Manga] = search_manga_by_name(
                memory.read_mangas(),
                selection_name
            )
            assert sel_manga is not None, f"Manga not found: {selection_name}"

            if sel_manga:
                if sel_manga.last_chapter:
                    await callback_query.message.edit_text(
                        LANG_DICT["cmd"]["info"]["done"] % (
                            sel_manga.name,
                            icons.LAST_ICON, sel_manga.last_chapter.name,
                            icons.CALENDAR_ICON, sel_manga.last_chapter.date,
                            icons.LINK_ICON, sel_manga.last_chapter.url
                        )
                    )

                else:
                    await callback_query.message.edit_text(
                        LANG_DICT["cmd"]["info"]["lastNotAvailable"]
                        % sel_manga.name
                    )
                    log(
                        "bot", "warn",
                        [
                            "cb_list_suscribed_mangas",
                            f"Last chapter not found for {selection_name}"
                        ]
                    )

            else:
                await callback_query.message.edit_text(
                    LANG_DICT["cmd"]["list"]["error"]
                )
                log("bot", "warn", [
                    "cb_list_suscribed_mangas",
                    f"Couldn't get info for {selection_name} and chat {chat.id}"
                ])

        elif selection in ['<', '>']:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)
            items: list[str] = [sc.manga.name for sc in sus]

            if selection == "<":
                page_num -= 1
            elif selection == ">":
                page_num += 1

            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["list"]["help"],
                reply_markup=pg_text_inline_keyboard(
                    me,
                    items,
                    3,
                    page_num
                )
            )

        elif selection == "X":
            await callback_query.message.edit_text(
                LANG_DICT["cmd"]["list"]["cancel"]
            )

        else:
            await callback_query.answer(LANG_DICT["cmd"]["list"]["error"])

    except Exception as e:
        log("bot", "error", [
            "cb_list_suscribed_mangas",
            f"List command callback failed: {str(e)}"
        ])
        await callback_query.answer(LANG_DICT["generic"]["error"])

###############################################################################
#                            CALLBACKS IDENTIFIERS                            #
###############################################################################

CALLBACK_MAP: dict[str, Callable[[Client, CallbackQuery], Awaitable[None]]] = {
    "tg_add_manga": cb_add_manga,
    "tg_del_manga": cb_del_manga,
    "tg_list_sc_mangas": cb_list_suscribed_mangas
}


@pyrogram_client.on_callback_query()
async def callback_router(client: Client, callback_query: CallbackQuery):
    """Routes the callback to the corresponding handler"""
    chat_id: int = callback_query.message.chat.id

    try:
        # Get the callback generator
        data: str = str(callback_query.data)
        caller: str = data.split(":")[0]

        # Get the handler
        handler: Optional[Callable[[Client, CallbackQuery], Awaitable[None]]] \
            = CALLBACK_MAP.get(caller, None)

        if handler:
            await handler(client, callback_query)
        else:
            log("bot", "warn", [
                "callback_router",
                f"Callback {caller} not found"
            ])
            await client.send_message(chat_id, LANG_DICT["generic"]["error"])

    except Exception as e:
        log("bot", "error", [
            "callback_router",
            f"Callback router failed: {str(e)}"
        ])
        await client.send_message(chat_id, LANG_DICT["generic"]["error"])
