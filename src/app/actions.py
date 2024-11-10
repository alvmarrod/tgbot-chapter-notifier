
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
    from domain.communications import Suscription
    from app.communications import notify_suscribers
    from app.client import pyrogram_client, memory


###############################################################################
#                                  MESSAGES                                   #
###############################################################################

async def process_reporting():
    """Reviews the last chapters and notifies the suscribers"""
    assert pyrogram_client is not None, "Pyrogram client is None"

    suscriptions: list[Suscription] = memory.read_suscriptions()
    mangas: list[Manga] = memory.read_mangas()

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

            await notify_suscribers(sus_manga.last_chapter, [sus.chat])

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
