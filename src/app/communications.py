
try:
    import src.utils as icons
    from src.domain.model import MangaChapter
    from src.domain.communications import Chat
    from src.app.client import pyrogram_client, LANG_DICT
except ModuleNotFoundError:
    import utils as icons
    from domain.model import MangaChapter
    from domain.communications import Chat
    from app.client import pyrogram_client, LANG_DICT


###############################################################################
#                                  MESSAGES                                   #
###############################################################################

async def notify_suscribers(chapter: MangaChapter, chats: list[Chat]):
    """Notifies the suscribers of a new chapter"""
    assert pyrogram_client is not None, "Pyrogram client is None"

    message: str = LANG_DICT["generic"]["newElement"] % (
        icons.NEW_ICON + icons.OK_ICON,
        chapter.name,
        chapter.manga,
        chapter.name,
        chapter.url
    )

    for chat in chats:
        await pyrogram_client.send_message(
            chat.id,
            message,
            disable_web_page_preview=True
        )
