import unittest
from typing import Optional

try:
    from src.utils import log
    import src.domain.communications as coms
except ModuleNotFoundError:
    from utils import log
    import domain.communications as coms


class TestDomainCommunications(unittest.TestCase):
    """Tests for the domain model"""

    def test_search_chat_by_id_ok(self):
        """A existing chat is searched and found by ID"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        found_chat: Optional[coms.Chat] = \
            coms.search_chat_by_id(chats, coms.Chat(2, "Chat 2"))

        assert found_chat is not None, "Chat not found"
        self.assertEqual(found_chat.id, 2)

    def test_search_chat_by_id_not_found(self):
        """A non existing chat is searched and not found by ID"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        found_chat: Optional[coms.Chat] = \
            coms.search_chat_by_id(chats, coms.Chat(4, "Chat 4"))

        self.assertIsNone(found_chat)

    def test_search_chat_by_id_empty_list(self):
        """An empty chat list is searched by ID"""
        chats: list[coms.Chat] = []

        found_chat: Optional[coms.Chat] = \
            coms.search_chat_by_id(chats, coms.Chat(1, "Chat 1"))

        self.assertIsNone(found_chat)

    def test_search_chat_by_id_empty_id(self):
        """A chat list is searched by an empty ID"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        found_chat: Optional[coms.Chat] = \
            coms.search_chat_by_id(chats, coms.Chat(0, "Chat 1"))
        self.assertIsNone(found_chat)

    def test_search_suscriptions_by_chat_id_ok(self):
        """A chat ID is searched and found in suscriptions"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        mangas: list[coms.Manga] = [
            coms.Manga("Manga 1", "link", None),
            coms.Manga("Manga 2", "link", None),
            coms.Manga("Manga 3", "link", None)
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], mangas[0], "1"),
            coms.Suscription(chats[1], mangas[1], "2"),
            coms.Suscription(chats[2], mangas[2], "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_chat_id(suscriptions, chats[1])

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 1)
        self.assertEqual(found_suscriptions[0].chat.id, 2)

    def test_search_suscriptions_by_chat_id_not_found(self):
        """A chat ID is searched and not found in suscriptions"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        mangas: list[coms.Manga] = [
            coms.Manga("Manga 1", "link", None),
            coms.Manga("Manga 2", "link", None),
            coms.Manga("Manga 3", "link", None)
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], mangas[0], "1"),
            coms.Suscription(chats[1], mangas[1], "2"),
            coms.Suscription(chats[2], mangas[2], "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_chat_id(suscriptions,
                                                coms.Chat(4, "Chat 4"))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_search_suscriptions_by_chat_id_empty_list(self):
        """An empty suscription list is searched by chat ID"""
        suscriptions: list[coms.Suscription] = []

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_chat_id(suscriptions,
                                                coms.Chat(1, "Chat 1"))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_search_suscriptions_by_chat_id_empty_id(self):
        """A suscription list is searched by an empty chat ID"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        mangas: list[coms.Manga] = [
            coms.Manga("Manga 1", "link", None),
            coms.Manga("Manga 2", "link", None),
            coms.Manga("Manga 3", "link", None)
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], mangas[0], "1"),
            coms.Suscription(chats[1], mangas[1], "2"),
            coms.Suscription(chats[2], mangas[2], "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_chat_id(suscriptions,
                                                coms.Chat(0, "Chat 1"))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_search_suscriptions_by_manga_ok(self):
        """A manga is searched and found in suscriptions"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        mangas: list[coms.Manga] = [
            coms.Manga("Manga 1", "", None),
            coms.Manga("Manga 2", "", None),
            coms.Manga("Manga 3", "", None)
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], mangas[0], "1"),
            coms.Suscription(chats[1], mangas[1], "2"),
            coms.Suscription(chats[2], mangas[2], "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_manga(suscriptions, mangas[1])

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 1)
        self.assertEqual(found_suscriptions[0].manga.name, "Manga 2")

    def test_search_suscriptions_by_manga_not_found(self):
        """A manga is searched and not found in suscriptions"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        mangas: list[coms.Manga] = [
            coms.Manga("Manga 1", "", None),
            coms.Manga("Manga 2", "", None),
            coms.Manga("Manga 3", "", None)
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], mangas[0], "1"),
            coms.Suscription(chats[1], mangas[1], "2"),
            coms.Suscription(chats[2], mangas[2], "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_manga(suscriptions,
                                              coms.Manga("Manga 4",
                                                         "link",
                                                         "4"))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_search_suscriptions_by_manga_empty_list(self):
        """An empty suscription list is searched by manga"""
        suscriptions: list[coms.Suscription] = []

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_manga(suscriptions,
                                              coms.Manga("Manga 1",
                                                         "link",
                                                         "1"))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_search_suscriptions_by_manga_empty_manga(self):
        """A suscription list is searched by an empty manga"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        suscriptions: list[coms.Suscription] = [
            coms.Suscription(chats[0], coms.Manga("Manga 1", "", None), "1"),
            coms.Suscription(chats[1], coms.Manga("Manga 2", "", None), "2"),
            coms.Suscription(chats[2], coms.Manga("Manga 3", "", None), "3")
        ]

        found_suscriptions: list[coms.Suscription] = \
            coms.search_suscriptions_by_manga(suscriptions,
                                              coms.Manga("", "", None))

        self.assertIsNotNone(found_suscriptions)
        self.assertEqual(len(found_suscriptions), 0)

    def test_add_chat_ok(self):
        """A chat is added to the chat list"""
        chats: list[coms.Chat] = []

        done: bool = coms.add_chat(chats, coms.Chat(1, "Chat 1"))

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 1)
        self.assertEqual(chats[0].id, 1)
        self.assertTrue(done)

    def test_add_chat_existing(self):
        """An existing chat is added to the chat list"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        done: bool = coms.add_chat(chats, coms.Chat(2, "Chat 2"))

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 3)
        self.assertFalse(done)

    def test_add_chat_empty_list(self):
        """A chat is added to an empty chat list"""
        chats: list[coms.Chat] = None

        done: bool = coms.add_chat(chats, coms.Chat(1, "Chat 1"))

        self.assertIsNone(chats)
        self.assertFalse(done)

    def test_add_chat_none_chat(self):
        """A None chat is added to the chat list"""
        chats: list[coms.Chat] = []

        done: bool = coms.add_chat(chats, None)

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 0)
        self.assertFalse(done)

    def test_del_chat_ok(self):
        """A chat is removed from the chat list"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        done: bool = coms.del_chat(chats, coms.Chat(2, "Chat 2"))

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 2)
        self.assertEqual(chats[0].id, 1)
        self.assertEqual(chats[1].id, 3)
        self.assertTrue(done)

    def test_del_chat_not_found(self):
        """A chat is removed from the chat list"""
        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        done: bool = coms.del_chat(chats, coms.Chat(4, "Chat 4"))

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 3)
        self.assertFalse(done)

    def test_del_chat_empty_list(self):
        """A chat is removed from an empty chat list"""
        chats: list[coms.Chat] = []

        done: bool = coms.del_chat(chats, coms.Chat(1, "Chat 1"))

        self.assertIsNotNone(chats)
        self.assertEqual(len(chats), 0)
        self.assertFalse(done)

    def test_del_chat_none_list(self):
        """A chat is removed from a None chat list"""
        chats: list[coms.Chat] = None

        done: bool = coms.del_chat(chats, coms.Chat(1, "Chat 1"))

        self.assertIsNone(chats)
        self.assertFalse(done)

    def test_add_suscription_ok(self):
        """A suscription is added to the suscription list"""
        suscriptions: list[coms.Suscription] = []

        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        manga: coms.Manga = coms.Manga("Manga 1", "link", "1")

        done: bool = coms.add_suscription(suscriptions, chats[1], manga)

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 1)
        self.assertEqual(suscriptions[0].chat.id, 2)
        self.assertEqual(suscriptions[0].manga.name, "Manga 1")
        self.assertTrue(done)

    def test_add_suscription_existing(self):
        """An existing suscription is added to the suscription list"""
        suscriptions: list[coms.Suscription] = [
            coms.Suscription(coms.Chat(1, "Chat 1"),
                             coms.Manga("Manga 1", "link", "1"),
                             "1"),
            coms.Suscription(coms.Chat(2, "Chat 2"),
                             coms.Manga("Manga 2", "link", "2"),
                             "2"),
            coms.Suscription(coms.Chat(3, "Chat 3"),
                             coms.Manga("Manga 3", "link", "3"),
                             "3")
        ]

        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        manga: coms.Manga = coms.Manga("Manga 2", "link", "2")

        done: bool = coms.add_suscription(suscriptions, chats[1], manga)

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 3)
        self.assertFalse(done)

    def test_add_suscription_empty_list(self):
        """A suscription is added to an empty suscription list"""
        suscriptions: list[coms.Suscription] = None

        chats: list[coms.Chat] = [
            coms.Chat(1, "Chat 1"),
            coms.Chat(2, "Chat 2"),
            coms.Chat(3, "Chat 3")
        ]

        manga: coms.Manga = coms.Manga("Manga 1", "link", "1")

        done: bool = coms.add_suscription(suscriptions, chats[1], manga)

        self.assertIsNone(suscriptions)
        self.assertFalse(done)

    def test_add_suscription_none_suscription(self):
        """A None suscription is added to the suscription list"""
        suscriptions: list[coms.Suscription] = []

        done: bool = coms.add_suscription(suscriptions, None, None)

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 0)
        self.assertFalse(done)

    def test_del_suscription_ok(self):
        """A suscription is removed from the suscription list"""
        suscriptions: list[coms.Suscription] = [
            coms.Suscription(coms.Chat(1, "Chat 1"),
                             coms.Manga("Manga 1", "link", "1"),
                             "1"),
            coms.Suscription(coms.Chat(2, "Chat 2"),
                             coms.Manga("Manga 2", "link", "2"),
                             "2"),
            coms.Suscription(coms.Chat(3, "Chat 3"),
                             coms.Manga("Manga 3", "link", "3"),
                             "3")
        ]

        done: bool = coms.del_suscription(
            suscriptions,
            coms.Chat(2, "Chat 2"),
            coms.Manga("Manga 2", "link", "2")
        )

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 2)
        self.assertEqual(suscriptions[0].chat.id, 1)
        self.assertEqual(suscriptions[1].chat.id, 3)
        self.assertTrue(done)

    def test_del_suscription_not_found(self):
        """A suscription is removed from the suscription list"""
        suscriptions: list[coms.Suscription] = [
            coms.Suscription(coms.Chat(1, "Chat 1"),
                             coms.Manga("Manga 1", "link", "1"),
                             "1"),
            coms.Suscription(coms.Chat(2, "Chat 2"),
                             coms.Manga("Manga 2", "link", "2"),
                             "2"),
            coms.Suscription(coms.Chat(3, "Chat 3"),
                             coms.Manga("Manga 3", "link", "3"),
                             "3")
        ]

        done: bool = coms.del_suscription(suscriptions,
                             coms.Chat(4, "Chat 4"),
                             coms.Manga("Manga 4", "link", "4"))

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 3)
        self.assertFalse(done)

    def test_del_suscription_empty_list(self):
        """A suscription is removed from an empty suscription list"""
        suscriptions: list[coms.Suscription] = []

        done: bool = coms.del_suscription(suscriptions,
                             coms.Chat(1, "Chat 1"),
                             coms.Manga("Manga 1", "link", "1"))

        self.assertIsNotNone(suscriptions)
        self.assertEqual(len(suscriptions), 0)
        self.assertFalse(done)

    def test_del_suscription_none_list(self):
        """A suscription is removed from a None suscription list"""
        suscriptions: list[coms.Suscription] = None

        done: bool = coms.del_suscription(suscriptions,
                             coms.Chat(1, "Chat 1"),
                             coms.Manga("Manga 1", "link", "1"))

        self.assertIsNone(suscriptions)
        self.assertFalse(done)


if __name__ == "__main__":
    unittest.main()
