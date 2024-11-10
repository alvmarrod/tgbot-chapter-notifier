import os
from typing import Optional
from sqlite3 import OperationalError

try:
    from src.utils import log
    from src.domain.domain_exception import DomainException
    from src.infrastructure.sqlite_client import SqliteManager
    from src.infrastructure.infra_exception import InfrastructureException
except ModuleNotFoundError:
    from utils import log
    from domain.domain_exception import DomainException
    from infrastructure.sqlite_client import SqliteManager
    from infrastructure.infra_exception import InfrastructureException

SQL_CREATE_CHATS_TABLE = '''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
'''

SQL_CREATE_SUSCRIPTIONS_TABLE = '''
    CREATE TABLE IF NOT EXISTS suscriptions (
        chat INTEGER NOT NULL,
        manga TEXT NOT NULL,
        last TEXT,
        PRIMARY KEY (chat, manga),
        FOREIGN KEY (chat) REFERENCES chats (id),
        FOREIGN KEY (manga) REFERENCES mangas (name)
    )
'''

SQL_CREATE_MANGA_CHAPTERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS manga_chapters (
        name TEXT NOT NULL,
        number TEXT,
        url TEXT,
        date TEXT,
        manga TEXT NOT NULL,
        PRIMARY KEY (manga, name),
        FOREIGN KEY (manga) REFERENCES mangas (name)
    )
'''

SQL_CREATE_MANGAS_TABLE = '''
    CREATE TABLE IF NOT EXISTS mangas (
        name TEXT PRIMARY KEY,
        url TEXT NOT NULL,
        last_chapter TEXT,
        FOREIGN KEY (last_chapter) REFERENCES manga_chapters (name)
    )
'''

SQL_READ_CHATS_TABLE = '''
    SELECT * FROM chats
'''

SQL_READ_CHATS_WHERE_ID = '''
    SELECT * FROM chats WHERE id = ?
'''

SQL_READ_SUS_TABLE = '''
    SELECT * FROM suscriptions
'''

SQL_READ_SUS_WHERE_CHAT = '''
    SELECT * FROM suscriptions WHERE chat = ?
'''

SQL_READ_SUS_WHERE_MANGA = '''
    SELECT * FROM suscriptions WHERE manga = ?
'''

SQL_READ_MANGA_CHAPTERS_TABLE = '''
    SELECT * FROM manga_chapters
'''

SQL_READ_MANGA_CHAPTERS_WHERE_MANGA_NAME = '''
    SELECT * FROM manga_chapters WHERE manga = ?
'''

SQL_READ_MANGAS_TABLE = '''
    SELECT * FROM mangas
'''

SQL_READ_MANGAS_WHERE_NAME = '''
    SELECT * FROM mangas WHERE name = ?
'''

SQL_INSERT_CHAT = '''
    INSERT INTO chats (id, name) VALUES (?, ?)
'''

SQL_INSERT_SUSCRIPTION = '''
    INSERT INTO suscriptions (chat, manga, last) VALUES (?, ?, ?)
'''

SQL_INSERT_MANGA_CHAPTER = '''
    INSERT INTO manga_chapters (name, number, url, date, manga)
    VALUES (?, ?, ?, ?, ?)
'''

SQL_INSERT_MANGA = '''
    INSERT INTO mangas (name, url, last_chapter) VALUES (?, ?, ?)
'''

SQL_DELETE_CHAT = '''
    DELETE FROM chats WHERE id = ?
'''

SQL_DELETE_SUSCRIPTION = '''
    DELETE FROM suscriptions WHERE chat = ? AND manga = ?
'''

SQL_DELETE_MANGA_CHAPTER = '''
    DELETE FROM manga_chapters WHERE name = ? AND manga = ?
'''

SQL_DELETE_MANGA = '''
    DELETE FROM mangas WHERE name = ?
'''

SQL_UPDATE_CHAT_NAME = '''
    UPDATE chats SET name = ? WHERE id = ?
'''

SQL_UPDATE_SUSCRIPTION_LAST = '''
    UPDATE suscriptions SET last = ? WHERE chat = ? AND manga = ?
'''

# SQL_UPDATE_MANGA_CHAPTER: Not happening

SQL_UPDATE_MANGA = '''
    UPDATE mangas SET last_chapter = ? WHERE name = ?
'''


class Database:
    """Class to manage the database operations with primitive types"""

    manager: SqliteManager

    def init(self, filepath: str) -> None:
        """Initializes the database"""
        try:
            db_path: str = filepath
            if not os.path.isabs(filepath):
                current_path: str = os.getcwd()
                db_path = os.path.join(current_path, filepath)

                log("bot", "debug",
                    [
                        "domain.database",
                        f"Relative database resolved to path: {db_path}"
                    ])

            self.manager = SqliteManager(db_path)

        except OperationalError as e:
            log("bot", "error", ["domain.database", f"Error initializing the database: {e}"])
            raise DomainException("Error initializing the database")

    def create(self) -> None:
        """Creates the database and the tables if they don't exist"""
        try:
            self.manager.exc_query(SQL_CREATE_CHATS_TABLE)
            self.manager.exc_query(SQL_CREATE_SUSCRIPTIONS_TABLE)
            self.manager.exc_query(SQL_CREATE_MANGA_CHAPTERS_TABLE)
            self.manager.exc_query(SQL_CREATE_MANGAS_TABLE)
        except InfrastructureException as e:
            log("bot", "error", ["domain.database", f"Error initializating the database: {e}"])
            raise DomainException("Error initializating the database")

    def read_chats(self) -> list[tuple[int, str]]:
        """Reads the chats table"""
        db_chats: list[tuple[str, ...]]
        chats: list[tuple[int, str]] = []

        db_chats = self.manager.read_query(SQL_READ_CHATS_TABLE)

        for chat in db_chats:
            chats.append((int(chat[0]), chat[1]))

        return chats

    def read_chat_by_id(self, id: int) -> Optional[tuple[int, str]]:
        """Reads the chats table"""
        chat: Optional[tuple[int, str]] = None
        db_chats: list[tuple[str, ...]]
        db_chats = self.manager.read_query(SQL_READ_CHATS_WHERE_ID, str(id,))

        if len(db_chats) > 1:
            log("bot", "warning",
                ["domain.database", f"More than one chat with the same ID: {id}"])

        if db_chats:
            chat = (int(db_chats[0][0]), db_chats[0][1])

        return chat

    def read_suscriptions(self) -> list[tuple[int, str, str]]:
        """Reads the suscriptions table"""
        db_suscriptions: list[tuple[str, ...]]
        suscriptions: list[tuple[int, str, str]] = []

        db_suscriptions = self.manager.read_query(SQL_READ_SUS_TABLE)

        for sus in db_suscriptions:
            suscriptions.append((int(sus[0]), sus[1], sus[2]))

        return suscriptions

    def read_suscription_by_chat(self, chat: int) -> \
            list[tuple[int, str, str]]:
        """Reads the suscriptions table"""
        db_suscriptions: list[tuple[str, ...]]
        suscriptions: list[tuple[int, str, str]] = []

        db_suscriptions = self.manager.read_query(SQL_READ_SUS_WHERE_CHAT,
                                                  str(chat,))

        for sus in db_suscriptions:
            suscriptions.append((int(sus[0]), sus[1], sus[2]))

        return suscriptions

    def read_suscription_by_manga(self, manga: str) -> \
            list[tuple[int, str, str]]:
        """Reads the suscriptions table"""
        db_suscriptions: list[tuple[str, ...]]
        suscriptions: list[tuple[int, str, str]] = []

        db_suscriptions = self.manager.read_query(SQL_READ_SUS_WHERE_MANGA,
                                                  str(manga,))

        for sus in db_suscriptions:
            suscriptions.append((int(sus[0]), sus[1], sus[2]))

        return suscriptions

    def read_manga_chapters(self) -> list[tuple[str, ...]]:
        """Reads the manga_chapters table"""
        db_manga_chapters: list[tuple[str, ...]]

        db_manga_chapters = self.manager.read_query(
            SQL_READ_MANGA_CHAPTERS_TABLE
        )

        return db_manga_chapters

    def read_manga_chapter_by_manga_name(self, name: str) -> \
            list[tuple[str, ...]]:
        """Reads the manga_chapters table"""
        db_manga_chapters: list[tuple[str, ...]]

        db_manga_chapters = self.manager.read_query(
            SQL_READ_MANGA_CHAPTERS_WHERE_MANGA_NAME,
            str(name,)
        )

        return db_manga_chapters

    def read_mangas(self) -> list[tuple[str, ...]]:
        """Reads the mangas table"""
        db_mangas: list[tuple[str, ...]]

        db_mangas = self.manager.read_query(SQL_READ_MANGAS_TABLE)

        return db_mangas

    def read_manga_by_name(self, name: str) -> list[tuple[str, ...]]:
        """Reads the mangas table"""
        db_mangas: list[tuple[str, ...]]

        db_mangas = self.manager.read_query(SQL_READ_MANGAS_WHERE_NAME,
                                            str(name,))

        return db_mangas

    def insert_chat(self, chat_id: int, chat_name: str) -> bool:
        """Inserts a chat in the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_INSERT_CHAT,
                                   str(chat_id), chat_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error inserting chat: {err}"])

        return done

    def insert_suscription(self, chat_id: int, manga_name: str,
                           last_chapter: str) -> bool:
        """Inserts a suscription in the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_INSERT_SUSCRIPTION,
                                   str(chat_id),
                                   manga_name,
                                   last_chapter)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database",
                 f"Error inserting suscription: {err}"]
                )

        return done

    def insert_manga_chapter(self, chapter_name: str,
                             chapter_number: str, chapter_url: str,
                             chapter_date: str, manga_name: str) -> bool:
        """Inserts a manga chapter in the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_INSERT_MANGA_CHAPTER,
                                   chapter_name, chapter_number,
                                   chapter_url, chapter_date, manga_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error inserting manga chapter: {err}"])

        return done

    def insert_manga(self, name: str, url: str, last_chapter: str = "") -> bool:
        """Inserts a manga in the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_INSERT_MANGA, name, url, last_chapter)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error inserting manga: {err}"])

        return done

    def delete_chat(self, id: int) -> bool:
        """Deletes a chat from the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_DELETE_CHAT, str(id))
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error deleting chat: {err}"])

        return done

    def delete_suscription(self, chat_id: int, manga_name: str) -> bool:
        """Deletes a suscription from the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_DELETE_SUSCRIPTION,
                                   str(chat_id), manga_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error deleting suscription: {err}"])

        return done

    def delete_manga_chapter(self, manga_name: str, chapter_name: str) -> bool:
        """Deletes a manga chapter from the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_DELETE_MANGA_CHAPTER,
                                   chapter_name, manga_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error deleting manga chapter: {err}"])

        return done

    def delete_manga(self, name: str) -> bool:
        """Deletes a manga from the database"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_DELETE_MANGA, name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error deleting manga: {err}"])

        return done

    def update_chat_name(self, id: int, name: str) -> bool:
        """Updates the name of a chat"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_UPDATE_CHAT_NAME, name, str(id))
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error updating chat name: {err}"])

        return done

    def update_suscription_last(self, chat_id: int, manga_name: str,
                                last_chapter: str) -> bool:
        """Updates the last chapter of a suscription"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_UPDATE_SUSCRIPTION_LAST, last_chapter,
                                   str(chat_id), manga_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error updating suscription last: {err}"])

        return done

    def update_manga(self, manga_name: str, last_chapter: str) -> bool:
        """Updates the last chapter of a manga"""
        done: bool = False
        try:
            self.manager.exc_query(SQL_UPDATE_MANGA, last_chapter, manga_name)
            done = True
        except InfrastructureException as err:
            log("bot", "error",
                ["domain.database", f"Error updating manga: {err}"])

        return done

    def close(self) -> None:
        """Closes the database"""
        self.manager.close()
