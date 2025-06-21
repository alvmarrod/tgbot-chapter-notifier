
from typing import Optional
from pyrogram.errors.exceptions.forbidden_403 import UserIsBlocked

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
    from src.app.client import pyrogram_client, memory
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
    from app.client import pyrogram_client, memory


###############################################################################
#                                  MESSAGES                                   #
###############################################################################

async def process_reporting() -> list[tuple[Suscription, Exception]]:
    """Reviews the last chapters and notifies the suscribers
    
    Returns the list of suscriptions paired with errors, aimed to detect
    problems like user blocks, etc
    """
    assert pyrogram_client is not None, "Pyrogram client is None"

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
                await notify_suscribers(sus_manga.last_chapter, [sus.chat])
            
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
                sus,
                notification_statuses[0][1]
            )

    return report


###############################################################################
#                                 ON MEMORY                                   #
###############################################################################

def delete_suscription(sus: Suscription) -> bool:
    """
    Wraps the full suscription deletion based on the suscription object
    """
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


def prune_suscriptions(suscriptions: list[tuple[Suscription, Exception]]):
    """
    Deletes a list of suscriptions based on their issues report
    """

    for sus, ex in suscriptions:

        if ex is None:
            continue

        if isinstance(ex, UserIsBlocked):
            ex: UserIsBlocked
            log(
                "bot",
                "error",
                [
                    "prune_suscriptions",
                    "Suscription obsolete due to User Blocked, pruning ongoing..."
                ]
            )
            log(
                "bot",
                "error",
                [
                    "prune_suscriptions",
                    f"{ex.MESSAGE}"
                ]
            )
            delete_suscription(sus)

        else:
            log(
                "bot",
                "warning",
                [
                    "prune_suscriptions",
                    f"Unmanaged error on suscription '{ex.__class__}': no action scheduled"
                ]
            )

###############################################################################
#                                  SCRAPPING                                  #
###############################################################################

def explore_web(url: str):
    """Explore the web and retrieve the information"""
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
