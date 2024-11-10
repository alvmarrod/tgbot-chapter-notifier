import unittest
from datetime import datetime

try:
    import src.domain.model as model
except ModuleNotFoundError:
    import domain.model as model


class TestDomainModel(unittest.TestCase):
    """Tests for the domain model"""

    def test_search_manga_by_name_ok(self):
        """A existing manga is searched and found by name"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_name(mangas, "Manga 2")

        self.assertIsNotNone(found_manga)

    def test_search_manga_by_name_not_found(self):
        """A non existing manga is searched and not found by name"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_name(mangas, "Manga 4")

        self.assertIsNone(found_manga)

    def test_search_manga_by_name_empty_list(self):
        """An empty manga list is searched by name"""
        mangas: list[model.Manga] = []

        found_manga: model.Manga = \
            model.search_manga_by_name(mangas, "Manga 1")

        self.assertIsNone(found_manga)

    def test_search_manga_by_name_empty_name(self):
        """A manga list is searched by an empty name"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_name(mangas, "")

        self.assertIsNone(found_manga)

    def test_search_manga_by_link_ok(self):
        """A existing manga is searched and found by link"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_link(mangas, "https://www.manga2.com")

        self.assertIsNotNone(found_manga)

    def test_search_manga_by_link_not_found(self):
        """A non existing manga is searched and not found by link"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_link(mangas, "https://www.manga4.com")

        self.assertIsNone(found_manga)

    def test_search_manga_by_link_empty_list(self):
        """An empty manga list is searched by link"""
        mangas: list[model.Manga] = []

        found_manga: model.Manga = \
            model.search_manga_by_link(mangas, "https://www.manga1.com")

        self.assertIsNone(found_manga)

    def test_search_manga_by_link_empty_link(self):
        """A manga list is searched by an empty link"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        found_manga: model.Manga = \
            model.search_manga_by_link(mangas, "")

        self.assertIsNone(found_manga)

    def test_search_chapter_in_list_ok(self):
        """An existing chapter is searched and found in the list"""
        chapters: list[model.MangaChapter] = [
            model.MangaChapter(
                "Chapter 1",
                "Chapter 1",
                "https://www.manga1.com/chapter1",
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                "Manga 1"
            ),
            model.MangaChapter(
                "Chapter 2",
                "Chapter 2",
                "https://www.manga1.com/chapter2",
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                "Manga 1"
            ),
            model.MangaChapter(
                "Chapter 1",
                "Chapter 1",
                "https://www.manga2.com/chapter1",
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                "Manga 2"
            ),
            model.MangaChapter(
                "Chapter 2",
                "Chapter 2",
                "https://www.manga2.com/chapter2",
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                "Manga 2"
            )
        ]

        chapter: model.MangaChapter = \
            model.MangaChapter(
                "Chapter 2",
                "Chapter 2",
                "https://www.manga2.com/chapter2",
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                "Manga 2"
            )

        found: bool = model.search_chapter_in_list(chapters, chapter)

        self.assertTrue(found)

    def test_search_chapter_in_list_not_found(self):
        """A non existing chapter is searched and not found in the list"""
        chapters: list[model.MangaChapter] = [
            model.MangaChapter(
                "Chapter 1",
                "Chapter 1",
                "https://www.manga1.com/chapter1",
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                "Manga 1"
            ),
            model.MangaChapter(
                "Chapter 2",
                "Chapter 2",
                "https://www.manga1.com/chapter2",
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                "Manga 1"
            ),
            model.MangaChapter(
                "Chapter 1",
                "Chapter 1",
                "https://www.manga2.com/chapter1",
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                "Manga 2"
            ),
            model.MangaChapter(
                "Chapter 2",
                "Chapter 2",
                "https://www.manga2.com/chapter2",
                datetime.strptime("2021-01-02", "%Y-%m-%d"),
                "Manga 2"
            )
        ]

        chapter: model.MangaChapter = \
            model.MangaChapter(
                "Chapter 3",
                "Chapter 3",
                "https://www.manga2.com/chapter3",
                datetime.strptime("2021-01-03", "%Y-%m-%d"),
                "Manga 2"
            )

        found: bool = model.search_chapter_in_list(chapters, chapter)

        self.assertFalse(found)

    def test_search_chapter_in_list_empty_list(self):
        """An empty chapter list is searched"""
        chapters: list[model.MangaChapter] = []

        chapter: model.MangaChapter = \
            model.MangaChapter(
                "Chapter 1",
                "Chapter 1",
                "https://www.manga1.com/chapter1",
                datetime.strptime("2021-01-01", "%Y-%m-%d"),
                "Manga 1"
            )

        found: bool = model.search_chapter_in_list(chapters, chapter)

        self.assertFalse(found)

    def test_add_manga_ok(self):
        """A manga is added to the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("Manga 4", "https://www.manga4.com",
                                         "444")

        done: bool = model.add_manga(mangas, manga)
        self.assertIn(manga, mangas)
        self.assertTrue(done)

    def test_add_manga_existing(self):
        """An existing manga is added to the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("Manga 2", "https://www.manga2.com",
                                         "222")

        done: bool = model.add_manga(mangas, manga)
        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_add_manga_empty_list(self):
        """A manga is added to an empty list"""
        mangas: list[model.Manga] = []

        manga: model.Manga = model.Manga("Manga 4", "https://www.manga4.com",
                                         "444")

        done: bool = model.add_manga(mangas, manga)
        self.assertIn(manga, mangas)
        self.assertTrue(done)

    def test_add_manga_none_list(self):
        """A manga is added to a None list"""
        mangas: list[model.Manga] = None

        manga: model.Manga = model.Manga("Manga 4", "https://www.manga4.com",
                                         "444")

        done: bool = model.add_manga(mangas, manga)
        self.assertIsNone(mangas)
        self.assertFalse(done)

    def test_add_manga_none_manga(self):
        """A None manga is added to the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = None
        done: bool = model.add_manga(mangas, manga)

        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_add_manga_empty_manga(self):
        """An empty manga is added to the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("", "", "")
        done: bool = model.add_manga(mangas, manga)

        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_del_manga_ok(self):
        """A manga is removed from the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("Manga 2", "https://www.manga2.com",
                                         "222")

        done: bool = model.del_manga(mangas, manga)
        
        self.assertNotIn(manga, mangas)
        self.assertTrue(done)

    def test_del_manga_not_found(self):
        """A manga is removed from the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("Manga 4", "https://www.manga4.com",
                                         "444")

        done: bool = model.del_manga(mangas, manga)

        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_del_manga_empty_list(self):
        """A manga is removed from an empty list"""
        mangas: list[model.Manga] = []

        manga: model.Manga = model.Manga("Manga 1", "https://www.manga1.com",
                                         "111")

        done: bool = model.del_manga(mangas, manga)

        self.assertEqual(0, len(mangas))
        self.assertFalse(done)

    def test_del_manga_none_list(self):
        """A manga is removed from a None list"""
        mangas: list[model.Manga] = None

        manga: model.Manga = model.Manga("Manga 1", "https://www.manga1.com",
                                         "111")

        done: bool = model.del_manga(mangas, manga)

        self.assertIsNone(mangas)
        self.assertFalse(done)

    def test_del_manga_none_manga(self):
        """A None manga is removed from the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = None
        done: bool = model.del_manga(mangas, manga)

        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_del_manga_empty_manga(self):
        """An empty manga is removed from the list"""
        mangas: list[model.Manga] = [
            model.Manga("Manga 1", "https://www.manga1.com", "111"),
            model.Manga("Manga 2", "https://www.manga2.com", "222"),
            model.Manga("Manga 3", "https://www.manga3.com", "333")
        ]

        manga: model.Manga = model.Manga("", "", "")
        done: bool = model.del_manga(mangas, manga)

        self.assertEqual(3, len(mangas))
        self.assertFalse(done)

    def test_dict_to_model(self):
        """A dictionary is converted to a list of MangaChapter"""
        data: dict[str, list[dict[str, str]]] = {
            "Manga 1": [
                {
                    "episode": "Chapter 1",
                    "url": "https://www.manga1.com/chapter1",
                    "date": "2021-01-01"
                },
                {
                    "episode": "Chapter 2",
                    "url": "https://www.manga1.com/chapter2",
                    "date": "2021-01-02"
                }
            ],
            "Manga 2": [
                {
                    "episode": "Chapter 1",
                    "url": "https://www.manga2.com/chapter1",
                    "date": "2021-01-01"
                },
                {
                    "episode": "Chapter 2",
                    "url": "https://www.manga2.com/chapter2",
                    "date": "2021-01-02"
                }
            ]
        }

        chapters: list[model.MangaChapter] = model.dict_to_model(data)

        self.assertEqual(4, len(chapters))

if __name__ == "__main__":
    unittest.main()
