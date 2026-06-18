from typing import Optional

try:
    from src.utils import log
    import src.infrastructure.web as it
    from src.domain.model import (
        Manga,
        dict_to_model,
        search_manga_by_name,
        MangaChapter,
        search_chapter_in_list
    )
    from src.domain.communications import Chat
    from src.domain.communications import Suscription
    from src.app.communications import notify_suscribers
    from src.app.client import memory
    from src.infrastructure.broker import ResponsePublisher
except ModuleNotFoundError:
    from utils import log
    import infrastructure.web as it
    from domain.model import (
        Manga,
        dict_to_model,
        search_manga_by_name,
        MangaChapter,
        search_chapter_in_list
    )
    from domain.communications import Chat
    from domain.communications import Suscription
    from app.communications import notify_suscribers
    from app.client import memory
    from infrastructure.broker import ResponsePublisher


async def process_reporting(
    publisher: Optional[ResponsePublisher] = None,
    bot_id: str = "",
) -> list[tuple[Suscription, Exception]]:
    suscriptions: list[Suscription] = memory.read_suscriptions()
    mangas: list[Manga] = memory.read_mangas()

    report: list[tuple[Suscription, Exception]] = []

    for sus in suscriptions:
        sus_manga: Optional[Manga] = search_manga_by_name(
            mangas,
            sus.manga.name
        )

        if not sus_manga:
            log("bot", "error", [
                "process_reporting",
                f"Suscription in chat {sus.chat.id} to unknown manga: "
                f"{sus.manga.name}"
            ])
            continue
        elif sus_manga.last_chapter is None:
            log("bot", "error", [
                "process_reporting",
                f"Last chapter for manga {sus.manga.name} not available"
            ])
            continue

        if not sus_manga.last_chapter or \
           sus.last != sus_manga.last_chapter.name:

            notification_statuses: list[tuple[Chat, Exception]] = \
                await notify_suscribers(
                    sus_manga.last_chapter,
                    [sus.chat],
                    publisher,
                    bot_id,
                )

            if notification_statuses[0][1] is None:
                if not memory.update_suscription_last(
                    chat_id=sus.chat.id,
                    manga_name=sus.manga.name,
                    last_chapter=sus_manga.last_chapter.name
                ):
                    log("bot", "warning", [
                        "process_reporting",
                        f"Last chapter updated for chat {sus.chat.id} and "
                        f"manga {sus.manga.name}"
                    ])

            report.append(
                (
                    sus,
                    notification_statuses[0][1]
                )
            )

    return report


def delete_suscription(sus: Suscription) -> bool:
    if sus is None:
        log(
            "bot",
            "info",
            [
                "delete_suscription",
                "A suscription was not provided: None"
            ]
        )

    else:
        return memory.delete_suscription(sus.chat.id, sus.manga.name)

    return False


def prune_suscriptions(
    suscriptions: list[tuple[Suscription, Exception]]
) -> None:
    for sus, ex in suscriptions:
        if ex is None:
            continue
        log(
            "bot",
            "warning",
            [
                "prune_suscriptions",
                f"Publish error on suscription '{sus}': "
                f"{ex.__class__.__name__}: {ex}"
            ]
        )


async def handle_delivery_error(error_body: dict) -> None:
    status = error_body.get("status")
    error_type = error_body.get("error_type", "")
    chat_id = error_body.get("chat_id")

    if status == "failed" and error_type == "USER_IS_BLOCKED" and chat_id:
        suscriptions: list[Suscription] = \
            memory.read_suscription_by_chat(chat_id)
        for sus in suscriptions:
            delete_suscription(sus)
        log(
            "bot",
            "error",
            [
                "handle_delivery_error",
                f"Pruned all subscriptions for blocked user chat {chat_id}"
            ]
        )

    elif status == "failed" and chat_id:
        log(
            "bot",
            "warning",
            [
                "handle_delivery_error",
                f"Delivery failed for chat {chat_id}: "
                f"{error_type} - {error_body.get('error_message', '')}"
            ]
        )


def explore_web(url: str):
    html: str = it.download_page(url)
    data: dict[str, list[dict[str, str]]] = it.parse_html(html)

    new_chapters: list[MangaChapter] = dict_to_model(data)

    if len(new_chapters) == 0:
        log("bot", "error", [
            "explore_web",
            "No chapters found on exploration"
        ])

    else:
        log("bot", "debug", [
            "explore_web",
            f"{len(new_chapters)} chapters found"
        ])

        mangas_in_memory: list[Manga] = memory.read_mangas()

        for chapter in new_chapters:
            if search_manga_by_name(mangas_in_memory, chapter.manga) is None:
                if memory.insert_manga(
                        name=chapter.manga,
                        url="",
                        last_chapter=None
                ):
                    log("bot", "info", [
                        "explore_web",
                        f"New manga {chapter.manga}"
                    ])
                else:
                    log("bot", "error", [
                        "explore_web",
                        f"Error saving new manga {chapter.manga}"
                    ])

            chapters: list[MangaChapter] = \
                memory.read_manga_chapter_by_manga_name(chapter.manga)

            if not search_chapter_in_list(chapters, chapter):
                if memory.insert_manga_chapter(
                    chapter_name=chapter.name,
                    chapter_number=chapter.number,
                    chapter_url=chapter.url,
                    chapter_date=chapter.date,
                    manga_name=chapter.manga,
                ):
                    log("bot", "info", [
                        "explore_web",
                        f"[{chapter.manga}] New chapter: {chapter.name}"
                    ])
                else:
                    log("bot", "error", [
                        "explore_web",
                        f"[{chapter.manga}] Error saving new chapter "
                        f"{chapter.name}"
                    ])
