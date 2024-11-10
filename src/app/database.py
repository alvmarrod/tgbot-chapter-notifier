from typing import Optional
from datetime import datetime

try:
    from src.utils import log
    from src.domain.model import Manga, MangaChapter
    from src.domain.communications import Chat, Suscription
    from src.domain.domain_exception import DomainException
    import src.domain.database as idb
except ModuleNotFoundError:
    from utils import log
    from domain.model import Manga, MangaChapter
    from domain.communications import Chat, Suscription
    from domain.domain_exception import DomainException
    import domain.database as idb

# TODO: review when to use/trigger raw_db.create() and manage the exceptions


class Database:
    """Class to manage the database operations with the appropiate model"""

    raw_db: idb.Database

    def init(self, filepath: str) -> None:
        """Initialize the database connection.
        Filepath should be relative path that will be later completed with
        the current working directory.
        """
        try:
            self.raw_db = idb.Database()
            self.raw_db.init(filepath)
            self.raw_db.create()
        except DomainException as err:
            log("bot", "error",
                ["app.database", f"Error initializing database: {err}"])
            raise err

    def read_chats(self) -> list[Chat]:
        """Reads the chats table"""
        db_chats: list[tuple[int, str]]
        model_chats: list[Chat] = []

        db_chats = self.raw_db.read_chats()

        for chat in db_chats:
            model_chats.append(Chat(chat[0], chat[1]))

        return model_chats

    def read_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        """Reads the chats table by ID"""
        db_chat: Optional[tuple[int, str]]
        model_chat: Optional[Chat] = None

        db_chat = self.raw_db.read_chat_by_id(chat_id)

        if db_chat:
            model_chat = Chat(db_chat[0], db_chat[1])

        return model_chat

    def read_suscriptions(self) -> list[Suscription]:
        """Reads the suscriptions table"""
        db_suscriptions: list[tuple[int, str, str]]
        model_suscriptions: list[Suscription] = []

        db_suscriptions = self.raw_db.read_suscriptions()

        model_chats: list[Chat] = self.read_chats()
        model_mangas: list[Manga] = self.read_mangas()

        for suscription in db_suscriptions:
            sus_chat: Chat = \
                next(filter(lambda x: x.id == suscription[0], model_chats))
            sus_manga: Manga = \
                next(filter(lambda x: x.name == suscription[1], model_mangas))
            model_suscriptions.append(
                Suscription(sus_chat, sus_manga, suscription[2])
            )

        return model_suscriptions

    def read_suscription_by_chat(self, chat_id: int) -> list[Suscription]:
        """Reads the suscriptions table by chat ID"""
        db_suscriptions: list[tuple[int, str, str]]
        model_suscriptions: list[Suscription] = []

        db_suscriptions = self.raw_db.read_suscription_by_chat(chat_id)

        model_chats: list[Chat] = self.read_chats()
        model_mangas: list[Manga] = self.read_mangas()

        for suscription in db_suscriptions:
            sus_chat: Chat = \
                next(filter(lambda x: x.id == suscription[0], model_chats))
            sus_manga: Manga = \
                next(filter(lambda x: x.name == suscription[1], model_mangas))
            model_suscriptions.append(
                Suscription(sus_chat, sus_manga, suscription[2])
            )

        return model_suscriptions

    def read_suscription_by_manga(self, manga: str) -> list[Suscription]:
        """Reads the suscriptions table by manga name"""
        db_suscriptions: list[tuple[int, str, str]]
        model_suscriptions: list[Suscription] = []

        db_suscriptions = self.raw_db.read_suscription_by_manga(manga)

        model_chats: list[Chat] = self.read_chats()
        model_mangas: list[Manga] = self.read_mangas()

        for suscription in db_suscriptions:
            sus_chat: Chat = \
                next(filter(lambda x: x.id == suscription[0], model_chats))
            sus_manga: Manga = \
                next(filter(lambda x: x.name == suscription[1], model_mangas))
            model_suscriptions.append(
                Suscription(sus_chat, sus_manga, suscription[2])
            )

        return model_suscriptions

    def read_manga_chapters(self) -> list[MangaChapter]:
        """Reads the manga_chapters table

        TODO: validate this datetime conversion"""
        db_manga_chapters: list[tuple[str, ...]]
        model_manga_chapters: list[MangaChapter] = []

        db_manga_chapters = self.raw_db.read_manga_chapters()

        for chapter in db_manga_chapters:
            model_manga_chapters.append(
                MangaChapter(
                    chapter[0],
                    chapter[1],
                    chapter[2],
                    datetime.strptime(chapter[3], "%Y-%m-%d %H:%M:%S"),
                    chapter[4]
                )
            )

        return model_manga_chapters

    def read_manga_chapter_by_manga_name(self, name: str) -> \
            list[MangaChapter]:
        """Reads the manga_chapters table by manga name"""
        db_manga_chapters: list[tuple[str, ...]]
        model_manga_chapters: list[MangaChapter] = []

        db_manga_chapters = self.raw_db.read_manga_chapter_by_manga_name(name)

        for chapter in db_manga_chapters:
            model_manga_chapters.append(
                MangaChapter(
                    chapter[0],
                    chapter[1],
                    chapter[2],
                    datetime.strptime(chapter[3], "%Y-%m-%d %H:%M:%S"),
                    chapter[4]
                )
            )

        return model_manga_chapters

    def read_mangas(self) -> list[Manga]:
        """Reads the mangas table"""
        db_mangas: list[tuple[str, ...]]
        model_mangas: list[Manga] = []

        db_mangas = self.raw_db.read_mangas()

        for manga in db_mangas:

            model_chapters: list[MangaChapter] = \
                self.read_manga_chapter_by_manga_name(manga[0])

            latest: Optional[MangaChapter] = None
            for chapter in model_chapters:
                if not latest or latest.date < chapter.date:
                    latest = chapter

            model_mangas.append(Manga(manga[0], manga[1], latest))

        return model_mangas

    def read_manga_by_name(self, name: str) -> list[Manga]:
        """Reads the mangas table by name"""
        db_mangas: list[tuple[str, ...]]
        model_mangas: list[Manga] = []

        db_mangas = self.raw_db.read_manga_by_name(name)

        for manga in db_mangas:

            model_chapters: list[MangaChapter] = \
                self.read_manga_chapter_by_manga_name(manga[0])

            latest: Optional[MangaChapter] = None
            for chapter in model_chapters:
                if not latest or latest.date < chapter.date:
                    latest = chapter

            model_mangas.append(Manga(manga[0], manga[1], latest))

        return model_mangas

    def insert_chat(self, chat_id: int, chat_name: str) -> bool:
        """Inserts a chat into the database"""
        done: bool = True

        if not self.raw_db.insert_chat(chat_id, chat_name):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't insert chat {chat_id}"])

        return done

    def insert_suscription(self, chat_id: int, manga_name: str,
                           last_chapter: str) -> bool:
        """Inserts a suscription into the database"""
        done: bool = True
        if not self.raw_db.insert_suscription(chat_id,
                                              manga_name, last_chapter):
            done = False
            log("bot", "error",
                [
                    "app.database",
                    f"Coudn't insert suscription for chat {chat_id}"])

        return done

    def insert_manga_chapter(self, chapter_name: str,
                             chapter_number: str, chapter_url: str,
                             chapter_date: datetime,
                             manga_name: str) -> bool:
        """Inserts a manga chapter into the database"""
        done: bool = True
        if not self.raw_db.insert_manga_chapter(
            chapter_name, chapter_number, chapter_url,
            datetime.strftime(chapter_date, "%Y-%m-%d %H:%M:%S"),
            manga_name
        ):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't insert chapter {chapter_name}"])

        return done

    def insert_manga(self, name: str, url: str,
                     last_chapter: Optional[str] = None) -> bool:
        """Inserts a manga into the database"""
        done: bool = True
        last_chapter = last_chapter if last_chapter else ""
        if not self.raw_db.insert_manga(name, url, last_chapter):
            done = False
            log("bot", "error",
                ["app.database", f"Couldn't insert manga {name}"])

        return done

    def delete_chat(self, chat_id: int) -> bool:
        """Deletes a chat from the database"""
        done: bool = True
        if not self.raw_db.delete_chat(chat_id):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't delete chat {chat_id}"])

        return done

    def delete_suscription(self, chat_id: int, manga_name: str) -> bool:
        """Deletes a suscription from the database"""
        done: bool = True
        if not self.raw_db.delete_suscription(chat_id, manga_name):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't delete suscription for chat {chat_id}"])

        return done

    def delete_manga_chapter(self, manga_name: str, chapter_name: str) -> bool:
        """Deletes a manga chapter from the database"""
        done: bool = True
        if not self.raw_db.delete_manga_chapter(manga_name, chapter_name):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't delete chapter {chapter_name}"])

        return done

    def delete_manga(self, name: str) -> bool:
        """Deletes a manga from the database"""
        done: bool = True
        if not self.raw_db.delete_manga(name):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't delete manga {name}"])

        return done

    def update_chat_name(self, chat_id: int, chat_name: str) -> bool:
        """Updates a chat name in the database"""
        done: bool = True
        if not self.raw_db.update_chat_name(chat_id, chat_name):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't update chat {chat_id}"])

        return done

    def update_suscription_last(self, chat_id: int, manga_name: str,
                                last_chapter: str) -> bool:
        """Updates a suscription last chapter in the database"""
        done: bool = True
        if not self.raw_db.update_suscription_last(
            chat_id, manga_name, last_chapter
        ):
            done = False
            log("bot", "error",
                ["app.database",
                 f"Coudn't update suscription for chat {chat_id}"])

        return done

    def update_manga_last(self, manga_name: str, last_chapter: str) -> bool:
        """Updates a manga in the database"""
        done: bool = True
        if not self.raw_db.update_manga(manga_name, last_chapter):
            done = False
            log("bot", "error",
                ["app.database", f"Coudn't update manga {manga_name}"])

        return done

    def close(self) -> None:
        """Closes the database connection"""
        self.raw_db.close()
