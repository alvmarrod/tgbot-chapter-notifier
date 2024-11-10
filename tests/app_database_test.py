import os
import unittest
from typing import Optional
from datetime import datetime

try:
    from src.utils import log
    import src.app.database as database
    from src.domain.model import Manga, MangaChapter
    from src.domain.communications import Chat, Suscription
except ModuleNotFoundError:
    from utils import log
    import app.database as database
    from domain.model import Manga, MangaChapter
    from domain.communications import Chat, Suscription


class TestAppDatabase(unittest.TestCase):
    """Tests for the app database module"""

    database_filepath: str = "tests/test_database.db"

    def tearDown(self) -> None:
        """Remove the test database file"""
        if os.path.exists(self.database_filepath):
            os.remove(self.database_filepath)

        return super().tearDown()

    def test_insert_chat(self) -> None:
        """Test the insert_chat method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        chat: Chat = Chat(1, "chat_name")
        memory.insert_chat(1, "chat_name")

        chats = memory.read_chats()
        self.assertEqual(len(chats), 1)
        self.assertEqual(chats[0], chat)

    def test_insert_suscription(self) -> None:
        """Test the insert_suscription method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_suscription(1, "manga_name", ""))

        manga: Manga = Manga("manga_name", "manga_url", None)
        chat: Chat = Chat(1, "chat_name")
        suscription: Suscription = Suscription(chat, manga, "")

        suscriptions = memory.read_suscriptions()
        self.assertEqual(len(suscriptions), 1)
        self.assertEqual(suscriptions[0], suscription)

    def test_insert_manga(self) -> None:
        """Test the insert_manga method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))

        manga: Manga = Manga("manga_name", "manga_url", None)

        mangas = memory.read_mangas()
        self.assertEqual(len(mangas), 1)
        self.assertEqual(mangas[0], manga)

    def test_insert_manga_chapter(self) -> None:
        """Test the insert_manga_chapter method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_manga_chapter(
            "chapter_name",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        ))

        manga_chapter: MangaChapter = MangaChapter(
            "chapter_name",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        )

        manga_chapters: list[MangaChapter] = memory.read_manga_chapters()

        self.assertEqual(len(manga_chapters), 1)
        self.assertEqual(manga_chapters[0].name, manga_chapter.name)
        self.assertEqual(manga_chapters[0].number, manga_chapter.number)
        self.assertEqual(manga_chapters[0].url, manga_chapter.url)
        self.assertEqual(manga_chapters[0].date, manga_chapter.date)
        self.assertEqual(manga_chapters[0].manga, manga_chapter.manga)

    def test_read_chat_by_id(self) -> None:
        """Test the read_chat_by_id method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))

        chat: Optional[Chat] = memory.read_chat_by_id(1)
        self.assertEqual(chat, Chat(1, "chat_name"))

    def test_read_suscription_by_chat(self) -> None:
        """Test the read_suscription_by_chat method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_suscription(1, "manga_name", ""))

        chat: Chat = Chat(1, "chat_name")
        manga: Manga = Manga("manga_name", "manga_url", None)
        suscription: Suscription = Suscription(chat, manga, "")

        suscriptions: list[Suscription] = memory.read_suscription_by_chat(1)
        self.assertEqual(len(suscriptions), 1)
        self.assertEqual(suscriptions[0], suscription)

    def test_read_suscription_by_manga(self) -> None:
        """Test the read_suscription_by_manga method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_suscription(1, "manga_name", ""))

        chat: Chat = Chat(1, "chat_name")
        manga: Manga = Manga("manga_name", "manga_url", None)
        suscription: Suscription = Suscription(chat, manga, "")

        suscriptions: list[Suscription] = \
            memory.read_suscription_by_manga("manga_name")
        self.assertEqual(len(suscriptions), 1)
        self.assertEqual(suscriptions[0], suscription)

    def test_read_manga_chapter_by_manga_name(self) -> None:
        """Test the read_manga_chapter_by_name method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_manga_chapter(
            "chapter_name",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        ))

        manga_chapter: MangaChapter = MangaChapter(
            "chapter_name",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        )

        chapters: list[MangaChapter] = \
            memory.read_manga_chapter_by_manga_name("manga_name")

        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0], manga_chapter)

    def test_read_manga_by_name(self) -> None:
        """Test the read_manga_by_name method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))

        manga: Manga = Manga("manga_name", "manga_url", None)

        mangas: list[Manga] = memory.read_manga_by_name("manga_name")
        self.assertEqual(len(mangas), 1)
        self.assertEqual(mangas[0], manga)

    def test_read_manga_by_name_not_exists(self) -> None:
        """Test the read_manga_by_name method with a non existing manga"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        mangas: list[Manga] = memory.read_manga_by_name("manga_name")
        self.assertEqual(len(mangas), 0)

    def test_delete_chat(self) -> None:
        """Test the delete_chat method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.delete_chat(1))

        chats = memory.read_chats()
        self.assertEqual(len(chats), 0)

    def test_delete_chat_not_exists(self) -> None:
        """Test the delete_chat method with a non existing chat"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(memory.delete_chat(1))

    def test_delete_suscription(self) -> None:
        """Test the delete_suscription method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_suscription(1, "manga_name", ""))

        self.assertTrue(memory.delete_suscription(1, "manga_name"))

        suscriptions = memory.read_suscriptions()
        self.assertEqual(len(suscriptions), 0)

    def test_delete_suscription_not_exists(self) -> None:
        """Test the delete_suscription method with a non
        existing suscription"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(memory.delete_suscription(1, "manga_name"))

    def test_delete_manga(self) -> None:
        """Test the delete_manga method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.delete_manga("manga_name"))

        mangas = memory.read_mangas()
        self.assertEqual(len(mangas), 0)

    def test_delete_manga_not_exists(self) -> None:
        """Test the delete_manga method with a non existing manga"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(memory.delete_manga("manga_name"))

    def test_delete_manga_chapter(self) -> None:
        """Test the delete_manga_chapter method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_manga_chapter(
            "chapter_name",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        ))

        self.assertTrue(
            memory.delete_manga_chapter("manga_name", "chapter_name")
        )

        manga_chapters = memory.read_manga_chapters()
        self.assertEqual(len(manga_chapters), 0)

    def test_delete_manga_chapter_not_exists(self) -> None:
        """Test the delete_manga_chapter method with a non
        existing manga chapter"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(
            memory.delete_manga_chapter("manga_name", "chapter_name")
        )

    def test_update_chat_name(self) -> None:
        """Test the update_chat_name method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.update_chat_name(1, "new_chat_name"))

        chat: Optional[Chat] = memory.read_chat_by_id(1)
        self.assertEqual(chat, Chat(1, "new_chat_name"))

    def test_update_chat_name_not_exists(self) -> None:
        """Test the update_chat_name method with a non existing chat"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(memory.update_chat_name(1, "new_chat_name"))

    def test_update_suscription_last(self) -> None:
        """Test the update_suscription_last method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_chat(1, "chat_name"))
        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_suscription(1, "manga_name", ""))

        self.assertTrue(memory.update_suscription_last(1, "manga_name", "1"))

        suscriptions = memory.read_suscriptions()
        self.assertEqual(len(suscriptions), 1)
        self.assertEqual(suscriptions[0].last, "1")

    def test_update_suscription_last_not_exists(self) -> None:
        """Test the update_suscription_last method with a non
        existing suscription"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(
            memory.update_suscription_last(1, "manga_name", "1")
        )

    def test_update_manga_last_chapter(self) -> None:
        """Test the update_manga_last_chapter method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertTrue(memory.insert_manga("manga_name", "manga_url", ""))
        self.assertTrue(memory.insert_manga_chapter(
            "chapter_name_test",
            "1",
            "chapter_url",
            datetime.strptime("2024-10-18 10:44:59", "%Y-%m-%d %H:%M:%S"),
            "manga_name"
        ))

        self.assertTrue(memory.update_manga_last("manga_name", "chapter_name_test"))

        mangas = memory.read_mangas()
        self.assertEqual(len(mangas), 1)
        self.assertIsNotNone(mangas[0].last_chapter)
        self.assertEqual(mangas[0].last_chapter.name, "chapter_name_test")

    def test_update_manga_last_chapter_not_exists(self) -> None:
        """Test the update_manga_last_chapter method with a non existing manga"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        self.assertFalse(
            memory.update_manga_last("manga_name", "chapter_name_test")
        )

    def test_close(self) -> None:
        """Test the close method"""

        memory: database.Database = database.Database()
        memory.init(self.database_filepath)

        memory.close()

        with self.assertRaises(Exception):
            memory.read_chats()

    def test_close_not_opened(self) -> None:
        """Test the close method without opening the database"""

        memory: database.Database = database.Database()

        with self.assertRaises(Exception):
            memory.close()
