import os
import unittest
from typing import Optional

try:
    import src.domain.database as database
except ModuleNotFoundError:
    import domain.database as database


class TestDomainDatabase(unittest.TestCase):
    """Tests for the domain database module"""

    database_filepath: str = "tests/test_database.db"

    def tearDown(self) -> None:
        """Tear down the test"""
        if os.path.exists(self.database_filepath):
            os.remove(self.database_filepath)

        return super().tearDown()

    def test_db_insert_chat(self):
        """Test the insert chat function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_chat(1, "Chat 1"))
        chats: list[tuple[int, str]] = memory.read_chats()

        self.assertEqual(chats[0][0], 1)
        self.assertEqual(chats[0][1], "Chat 1")

    def test_db_insert_suscription(self):
        """Test the insert suscription function"""
        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        aux_chat: tuple[int, str] = (1111, "Chat 1")
        aux_manga: tuple[str, ...] = ("Manga 1", "url", "")
        self.assertTrue(memory.insert_chat(*aux_chat))
        self.assertTrue(memory.insert_manga(*aux_manga))

        self.assertTrue(memory.insert_suscription(
            aux_chat[0], aux_manga[0], "")
        )

        suscriptions: list[tuple[int, str, str]] = memory.read_suscriptions()

        self.assertEqual(suscriptions[0][0], 1111)
        self.assertEqual(suscriptions[0][1], "Manga 1")
        self.assertEqual(suscriptions[0][2], "")

    def test_db_insert_manga(self):
        """Test the insert manga function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        mangas: list[tuple[str, ...]] = memory.read_mangas()

        self.assertEqual(mangas[0][0], "Manga 1")
        self.assertEqual(mangas[0][1], "url")

    def test_db_insert_manga_chapter(self):
        """Test the insert manga chapter function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(
            memory.insert_manga_chapter(
                "Chapter 1", "1",
                "url", "date",
                "Manga 1"
            )
        )

        chapters: list[tuple[str, ...]] = memory.read_manga_chapters()

        self.assertEqual(chapters[0][0], "Chapter 1")
        self.assertEqual(chapters[0][1], "1")
        self.assertEqual(chapters[0][2], "url")
        self.assertEqual(chapters[0][3], "date")
        self.assertEqual(chapters[0][4], "Manga 1")

    def test_db_read_chat_by_id(self):
        """Test the read chat by id function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_chat(1, "Chat 1"))
        chat: Optional[tuple[int, str]] = memory.read_chat_by_id(1)

        assert chat is not None

        self.assertEqual(chat[0], 1)
        self.assertEqual(chat[1], "Chat 1")

    def test_db_read_suscription_by_chat(self):
        """Test the read suscription by chat function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        aux_chat: tuple[int, str] = (1111, "Chat 1")
        aux_manga: tuple[str, ...] = ("Manga 1", "url", "")
        self.assertTrue(memory.insert_chat(*aux_chat))
        self.assertTrue(memory.insert_manga(*aux_manga))

        self.assertTrue(
            memory.insert_suscription(
                aux_chat[0],
                aux_manga[0],
                ""
            )
        )

        suscriptions: list[tuple[int, str, str]] = \
            memory.read_suscription_by_chat(1111)

        self.assertEqual(suscriptions[0][0], 1111)
        self.assertEqual(suscriptions[0][1], "Manga 1")
        self.assertEqual(suscriptions[0][2], "")

    def test_db_read_suscription_by_manga(self):
        """Test the read suscription by manga function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        aux_chat: tuple[int, str] = (1111, "Chat 1")
        aux_manga: tuple[str, ...] = ("Manga 1", "url", "")
        self.assertTrue(memory.insert_chat(*aux_chat))
        self.assertTrue(memory.insert_manga(*aux_manga))

        self.assertTrue(
            memory.insert_suscription(aux_chat[0], aux_manga[0], "")
        )

        suscriptions: list[tuple[int, str, str]] = \
            memory.read_suscription_by_manga("Manga 1")

        self.assertEqual(suscriptions[0][0], 1111)
        self.assertEqual(suscriptions[0][1], "Manga 1")
        self.assertEqual(suscriptions[0][2], "")

    def test_db_read_manga_chapter_by_manga_name(self):
        """Test the read manga chapter by name function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))

        self.assertTrue(memory.insert_manga_chapter(
                chapter_name="Chapter 1",
                chapter_number="1",
                chapter_url="url",
                chapter_date="date",
                manga_name="Manga 1"
            )
        )

        chapters: list[tuple[str, ...]] = \
            memory.read_manga_chapter_by_manga_name("Manga 1")

        self.assertEqual(chapters[0][0], "Chapter 1")
        self.assertEqual(chapters[0][1], "1")
        self.assertEqual(chapters[0][2], "url")
        self.assertEqual(chapters[0][3], "date")
        self.assertEqual(chapters[0][4], "Manga 1")

    def test_db_read_manga_by_name(self):
        """Test the read manga by name function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        mangas: list[tuple[str, ...]] = memory.read_manga_by_name("Manga 1")

        self.assertEqual(mangas[0][0], "Manga 1")
        self.assertEqual(mangas[0][1], "url")

    def test_db_delete_chat(self):
        """Test the delete chat function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_chat(1, "Chat 1"))
        self.assertTrue(memory.delete_chat(1))
        chats = memory.read_chats()
        self.assertEqual(len(chats), 0)

    def test_db_delete_suscription(self):
        """Test the delete suscription function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        aux_chat: tuple[int, str] = (1111, "Chat 1")
        aux_manga: tuple[str, ...] = ("Manga 1", "url", "")
        self.assertTrue(memory.insert_chat(*aux_chat))
        self.assertTrue(memory.insert_manga(*aux_manga))

        self.assertTrue(
            memory.insert_suscription(aux_chat[0], aux_manga[0], "")
        )
        self.assertTrue(
            memory.delete_suscription(aux_chat[0], aux_manga[0])
        )

        suscriptions = memory.read_suscriptions()

        self.assertEqual(len(suscriptions), 0)

    def test_db_delete_manga(self):
        """Test the delete manga function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        self.assertTrue(memory.delete_manga("Manga 1"))

        mangas = memory.read_mangas()
        self.assertEqual(len(mangas), 0)

    def test_db_delete_manga_chapter(self):
        """Test the delete manga chapter function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        self.assertTrue(memory.insert_manga_chapter(
            chapter_name="Chapter 1",
            chapter_number="1",
            chapter_url="url",
            chapter_date="date",
            manga_name="Manga 1"
            )
        )

        self.assertTrue(memory.delete_manga_chapter("Manga 1", "Chapter 1"))

        chapters = memory.read_manga_chapters()
        self.assertEqual(len(chapters), 0)

    def test_db_update_chat_name(self):
        """Test the update chat function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_chat(10, "Chat 1"))
        self.assertTrue(memory.update_chat_name(10, "Chat 2"))

        chats: list[tuple[int, str]] = memory.read_chats()
        self.assertEqual(chats[0][0], 10)
        self.assertEqual(chats[0][1], "Chat 2")

    def test_db_update_suscription_last(self):
        """Test the update suscription function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        aux_chat: tuple[int, str] = (155, "Chat 1")
        aux_manga: tuple[str, ...] = ("Manga 38", "url")
        self.assertTrue(memory.insert_chat(*aux_chat))
        self.assertTrue(memory.insert_manga(*aux_manga))

        self.assertTrue(
            memory.insert_suscription(aux_chat[0], aux_manga[0], "")
        )

        self.assertTrue(
            memory.update_suscription_last(
                aux_chat[0],
                aux_manga[0],
                "New chapter"
            )
        )
        suscriptions: list[tuple[int, str, str]] = memory.read_suscriptions()

        self.assertEqual(suscriptions[0][0], 155)
        self.assertEqual(suscriptions[0][1], "Manga 38")
        self.assertEqual(suscriptions[0][2], "New chapter")

    def test_db_update_manga_last(self):
        """Test the update manga function"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        self.assertTrue(memory.update_manga("Manga 1", "New Chapter"))

        mangas: list[tuple[str, ...]] = memory.read_mangas()

        self.assertEqual(mangas[0][0], "Manga 1")
        self.assertEqual(mangas[0][1], "url")
        self.assertEqual(mangas[0][2], "New Chapter")

    def test_db_update_manga_last_no_manga(self):
        """Test the update manga function without manga"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertFalse(
            memory.update_manga("Manga 1", "New Chapter")
        )

    def test_db_update_manga_last_no_manga_chapter(self):
        """Test the update manga function without manga chapter"""

        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        self.assertTrue(memory.insert_manga("Manga 1", "url"))
        self.assertFalse(
            memory.update_manga("Manga 2", "New Chapter")
        )

    def test_close(self):
        """Test the close function"""    
        memory: database.Database = database.Database()

        memory.init(self.database_filepath)
        memory.create()

        memory.close()

    def test_close_no_connection(self):
        """Test the close function without connection"""
        memory: database.Database = database.Database()

        with self.assertRaises(Exception):
            memory.close()
