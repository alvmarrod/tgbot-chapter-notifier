
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

async def notify_suscribers(chapter: MangaChapter, chats: list[Chat]) \
    -> list[tuple[Chat, Exception]]:
    """Notifies the suscribers of a new chapter
    
    Returns a list with the status returned by each Chat notification, based
    on exceptions

    Possible execeptions:
    - Can raise
      - pyrogram.errors.exceptions.forbidden_403.UserIsBlocked
    """
    assert pyrogram_client is not None, "Pyrogram client is None"
    results: list[tuple[Chat, Exception]] = []

    message: str = LANG_DICT["generic"]["newElement"] % (
        icons.NEW_ICON + icons.OK_ICON,
        chapter.name,
        chapter.manga,
        chapter.name,
        chapter.url
    )

    for chat in chats:
        try:
            await pyrogram_client.send_message(
                chat.id,
                message,
                disable_web_page_preview=True
            )
            results.append((chat, None))
        except Exception as err:
            results.append((chat, err))

    return results
