"""Module in charge to define the model to represent the objects for the app"""
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

try:
    from src.utils import log
    from src.domain.domain_exception import DomainException
except ModuleNotFoundError:
    from utils import log
    from domain.domain_exception import DomainException


@dataclass
class MangaChapter():
    """Models a manga chapter.

    - Chapter name (if any)(NOT manga name)
    - Number, string because some chapters are not trutly numeric
    - A link (html)
    - Date as datetime
    - Manga to which it belongs
    """
    name:   str
    number: str
    url:    str
    date:   datetime
    manga:  str


@dataclass
class Manga():
    """Models a manga.

    - Name
    - A link (html)
    - Last chapter, string because some chapters are not trutly numeric
    """
    name:   str
    link:   str
    last_chapter: Optional[MangaChapter]


##############################################################################
#                                  LOW LEVEL                                 #
##############################################################################

def search_manga_by_name(mangas: list[Manga], name: str) -> Optional[Manga]:
    """Searchs the manga list by provided name"""
    item: Optional[Manga] = None
    for manga in mangas:
        if manga.name == name:
            item = manga
            break

    return item


def search_manga_by_link(mangas: list[Manga], link: str) -> Optional[Manga]:
    """Searchs the manga list by provided link"""
    item: Optional[Manga] = None
    for manga in mangas:
        if manga.link == link:
            item = manga
            break

    return item


def search_chapter_in_list(chapters: list[MangaChapter],
                           chapter: MangaChapter) -> bool:
    """Searchs the chapter list by provided chapter"""
    found: bool = False
    for ch in chapters:
        if ch.name == chapter.name and ch.number == chapter.number:
            found = True
            break

    return found

##############################################################################
#                               INTERMEDIATE                                 #
##############################################################################


def add_manga(mangas: list[Manga], manga: Manga) -> bool:
    """Adds a manga to the system"""
    created: bool = False

    try:
        if manga is None or \
            manga.name is None or manga.name == "" or \
                manga.link is None or manga.link == "":
            raise DomainException("Manga name and link are required")

        if search_manga_by_name(mangas, manga.name) is not None:
            raise DomainException("Manga already exists")

        mangas.append(manga)
        created = True

    except DomainException as err:
        log("bot", "err", ["add_manga", " Couldn't add manga"])
        log("bot", "info", ["add_manga", f" {str(err)}"])

    except Exception as err:
        log("bot", "err", ["add_manga", " Couldn't add manga"])
        log("bot", "debug", ["add_manga", f" {str(err)}"])

    return created


def del_manga(mangas: list[Manga], manga: Manga) -> bool:
    """Removes a manga from the system."""
    deleted: bool = False

    try:
        if manga is None or \
                manga.name is None or manga.name == "":
            raise DomainException("Mangas list is not initialized")

        target_manga: Optional[Manga] = search_manga_by_name(mangas,
                                                             manga.name)
        if not target_manga:
            raise DomainException(f" Couldn't find manga: {manga.name}")

        mangas.remove(target_manga)
        deleted = True

    except DomainException as err:
        log("bot", "err", ["del_manga", " Couldn't remove manga"])
        log("bot", "info", ["del_manga", f" {str(err)}"])

    except Exception as err:
        log("bot", "err", ["del_manga", " Couldn't remove manga"])
        log("bot", "debug", ["del_manga", f" {str(err)}"])

    return deleted


def dict_to_model(data: dict[str, list[dict[str, str]]]) -> list[MangaChapter]:
    """Converts a dictionary to a list of Manga objects"""
    chapters: list[MangaChapter] = []

    for manga, chapters_list in data.items():
        for chapter in chapters_list:
            chapters.append(
                MangaChapter(
                    name=chapter["episode"],
                    number=chapter["episode"],
                    url=chapter["url"],
                    date=datetime.now(),
                    manga=manga
                )
            )

    return chapters
