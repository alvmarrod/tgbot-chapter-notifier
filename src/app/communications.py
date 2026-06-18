try:
    import src.utils as icons
    from src.domain.model import MangaChapter
    from src.domain.communications import Chat
    from src.app.client import LANG_DICT, ERROR_QUEUE
    from src.infrastructure.broker import ResponsePublisher
except ModuleNotFoundError:
    import utils as icons
    from domain.model import MangaChapter
    from domain.communications import Chat
    from app.client import LANG_DICT, ERROR_QUEUE
    from infrastructure.broker import ResponsePublisher


async def notify_suscribers(
    chapter: MangaChapter,
    chats: list[Chat],
    publisher: ResponsePublisher,
    bot_id: str,
) -> list[tuple[Chat, Exception]]:
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
            await publisher.publish_text(
                chat_id=chat.id,
                text=message,
                disable_web_page_preview=True,
                reply_to=ERROR_QUEUE,
            )
            results.append((chat, None))
        except Exception as err:
            results.append((chat, err))

    return results
