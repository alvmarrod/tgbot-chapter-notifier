from typing import Optional, Callable, Awaitable

try:
    from src.utils import log
    import src.utils as icons
    from src.app.client import memory, LANG_DICT
    from src.app.actions import delete_suscription
    from src.domain.model import Manga, search_manga_by_name
    import src.domain.communications as comms
    from src.app.messages import (
        pg_text_inline_keyboard,
        pg_get_element_by_position
    )
    from src.app.dispatcher import Responder
except ModuleNotFoundError:
    from utils import log
    import utils as icons
    from app.client import memory, LANG_DICT
    from app.actions import delete_suscription
    from domain.model import Manga, search_manga_by_name
    import domain.communications as comms
    from app.messages import (
        pg_text_inline_keyboard,
        pg_get_element_by_position
    )
    from app.dispatcher import Responder


async def start(
    responder: Responder,
    chat_id: int,
    **kwargs,
) -> None:
    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)

        if not chat:
            memory.insert_chat(chat_id, "")
            await responder.reply_text(LANG_DICT["cmd"]["start"]["done"])
        else:
            await responder.reply_text(LANG_DICT["cmd"]["start"]["error"])

    except Exception as e:
        log("bot", "error", ["start", f"Start command failed: {str(e)}"])
        await responder.reply_text(LANG_DICT["generic"]["error"])


async def trigger_add_manga(
    responder: Responder,
    chat_id: int,
    **kwargs,
) -> None:
    me: str = "tg_add_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)

        if chat is None:
            await responder.send_message(
                chat_id, LANG_DICT["generic"]["notStarted"]
            )
        else:
            page_num: int = 0
            items: list[str] = [manga.name for manga in memory.read_mangas()]

            await responder.send_message(
                chat_id,
                LANG_DICT["cmd"]["add"]["help"],
                reply_markup=pg_text_inline_keyboard(me, items, 3, page_num),
            )

    except Exception as e:
        log("bot", "error",
            ["trigger_add_manga", f"Add command failed: {str(e)}"])
        await responder.reply_text(LANG_DICT["generic"]["error"])


async def cb_add_manga(
    responder: Responder,
    chat_id: int,
    callback_data: str,
    **kwargs,
) -> None:
    me: str = "tg_add_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_data).split(":")[-1])
        selection: str = str(callback_data).split(":")[1]

        if selection not in ['<', '>', 'X']:
            mangas: list[str] = [manga.name for manga in memory.read_mangas()]

            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

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
                await responder.edit_text(
                    LANG_DICT["cmd"]["add"]["error"] % selection_name
                )
                raise Exception("Suscription for this manga already exists")

            if memory.insert_suscription(
                chat_id=chat.id,
                manga_name=sel_manga.name,
                last_chapter=""
            ):
                await responder.answer_callback(
                    LANG_DICT["cmd"]["add"]["done"]
                )
                await responder.edit_text(
                    LANG_DICT["cmd"]["add"]["selection"] % selection_name
                )
                log(
                    "bot", "info",
                    [
                        "cb_add_manga",
                        f"Added manga '{selection_name}' to chat '{chat.id}'"
                    ]
                )
            else:
                await responder.answer_callback(
                    LANG_DICT["cmd"]["add"]["error"] % selection_name
                )
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

            await responder.edit_text(
                LANG_DICT["cmd"]["add"]["help"],
                reply_markup=pg_text_inline_keyboard(me, items, 3, page_num),
            )

        elif selection == "X":
            await responder.edit_text(
                LANG_DICT["cmd"]["add"]["cancel"]
            )

        else:
            await responder.answer_callback(
                LANG_DICT["cmd"]["add"]["error"]
            )

    except Exception as e:
        log("bot", "error", [
            "cb_add_manga",
            f"Add command callback failed: {str(e)}"
        ])
        await responder.answer_callback(LANG_DICT["generic"]["error"])


async def trigger_del_manga(
    responder: Responder,
    chat_id: int,
    **kwargs,
) -> None:
    me: str = "tg_del_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)

        if chat is None:
            await responder.send_message(
                chat_id, LANG_DICT["generic"]["notStarted"]
            )
        else:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            if len(sus) == 0:
                await responder.reply_text(LANG_DICT["cmd"]["del"]["empty"])
            else:
                items: list[str] = [sc.manga.name for sc in sus]

                await responder.reply_text(
                    LANG_DICT["cmd"]["del"]["help"],
                    reply_markup=pg_text_inline_keyboard(me, items, 3, 0),
                )

    except Exception as e:
        log("bot", "error",
            ["cb_del_manga", f"Del command failed: {str(e)}"])
        await responder.reply_text(LANG_DICT["generic"]["error"])


async def cb_del_manga(
    responder: Responder,
    chat_id: int,
    callback_data: str,
    **kwargs,
) -> None:
    me: str = "tg_del_manga"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_data).split(":")[-1])
        selection: str = str(callback_data).split(":")[1]

        if selection not in ['<', '>', 'X']:
            my_sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            mangas: list[str] = [sc.manga.name for sc in my_sus]

            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

            target_sus: Optional[comms.Suscription] = \
                next((sc for sc in my_sus if sc.manga.name == selection_name),
                     None)

            if delete_suscription(target_sus):
                await responder.answer_callback(
                    LANG_DICT["cmd"]["del"]["done"]
                )
                await responder.edit_text(
                    LANG_DICT["cmd"]["del"]["selection"] % selection_name
                )
                log(
                    "bot", "info",
                    [
                        "cb_del_manga",
                        f"Deleted manga {selection_name} from chat {chat.id}"
                    ]
                )
            else:
                await responder.answer_callback(
                    LANG_DICT["cmd"]["del"]["error"]
                )
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

            await responder.edit_text(
                LANG_DICT["cmd"]["del"]["help"],
                reply_markup=pg_text_inline_keyboard(me, items, 3, page_num),
            )

        elif selection == "X":
            await responder.edit_text(
                LANG_DICT["cmd"]["del"]["cancel"]
            )

        else:
            await responder.answer_callback(
                LANG_DICT["cmd"]["del"]["error"]
            )

    except Exception as e:
        log("bot", "error", [
            "cb_del_manga",
            f"Del command callback failed: {str(e)}"
        ])
        await responder.answer_callback(LANG_DICT["generic"]["error"])


async def trigger_list_suscribed_mangas(
    responder: Responder,
    chat_id: int,
    **kwargs,
) -> None:
    me: str = "tg_list_sc_mangas"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)

        if chat is None:
            await responder.send_message(
                chat_id, LANG_DICT["generic"]["notStarted"]
            )
        else:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            if len(sus) == 0:
                await responder.reply_text(
                    LANG_DICT["cmd"]["list"]["empty"]
                )
            else:
                await responder.reply_text(
                    LANG_DICT["cmd"]["list"]["done"],
                    reply_markup=pg_text_inline_keyboard(
                        me,
                        [sc.manga.name for sc in sus],
                        3,
                        0,
                    ),
                )

    except Exception as e:
        log("bot", "error",
            ["list_mangas", f"List command failed: {str(e)}"])
        await responder.reply_text(LANG_DICT["generic"]["error"])


async def cb_list_suscribed_mangas(
    responder: Responder,
    chat_id: int,
    callback_data: str,
    **kwargs,
) -> None:
    me: str = "tg_list_sc_mangas"

    try:
        chat: Optional[comms.Chat] = memory.read_chat_by_id(chat_id)
        assert chat is not None, f"Chat not found: {chat_id}"

        page_num: int = int(str(callback_data).split(":")[-1])
        selection: str = str(callback_data).split(":")[1]

        if selection not in ['<', '>', 'X']:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)

            mangas: list[str] = [sc.manga.name for sc in sus]
            selection_name: str = \
                pg_get_element_by_position(mangas, page_num, int(selection))

            sel_manga: Optional[Manga] = search_manga_by_name(
                memory.read_mangas(),
                selection_name
            )
            assert sel_manga is not None, f"Manga not found: {selection_name}"

            if sel_manga:
                if sel_manga.last_chapter:
                    await responder.edit_text(
                        LANG_DICT["cmd"]["info"]["done"] % (
                            sel_manga.name,
                            icons.LAST_ICON, sel_manga.last_chapter.name,
                            icons.CALENDAR_ICON, sel_manga.last_chapter.date,
                            icons.LINK_ICON, sel_manga.last_chapter.url
                        )
                    )
                else:
                    await responder.edit_text(
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
                await responder.edit_text(
                    LANG_DICT["cmd"]["list"]["error"]
                )
                log("bot", "warn", [
                    "cb_list_suscribed_mangas",
                    f"Couldn't get info for {selection_name} and chat {chat_id}"
                ])

        elif selection in ['<', '>']:
            sus: list[comms.Suscription] = \
                memory.read_suscription_by_chat(chat_id)
            items: list[str] = [sc.manga.name for sc in sus]

            if selection == "<":
                page_num -= 1
            elif selection == ">":
                page_num += 1

            await responder.edit_text(
                LANG_DICT["cmd"]["list"]["help"],
                reply_markup=pg_text_inline_keyboard(me, items, 3, page_num),
            )

        elif selection == "X":
            await responder.edit_text(
                LANG_DICT["cmd"]["list"]["cancel"]
            )

        else:
            await responder.answer_callback(
                LANG_DICT["cmd"]["list"]["error"]
            )

    except Exception as e:
        log("bot", "error", [
            "cb_list_suscribed_mangas",
            f"List command callback failed: {str(e)}"
        ])
        await responder.answer_callback(LANG_DICT["generic"]["error"])


CALLBACK_MAP: dict[
    str,
    Callable[..., Awaitable[None]]
] = {
    "tg_add_manga": cb_add_manga,
    "tg_del_manga": cb_del_manga,
    "tg_list_sc_mangas": cb_list_suscribed_mangas,
}

COMMAND_MAP: dict[str, Callable[..., Awaitable[None]]] = {
    "start": start,
    "add": trigger_add_manga,
    "del": trigger_del_manga,
    "list": trigger_list_suscribed_mangas,
}
