import unittest

try:
    import src.app.messages as msgs
except ModuleNotFoundError:
    import app.messages as msgs


class TestAppMessages(unittest.TestCase):
    """Tests for the app messages"""

    def test_page_items_empty_list(self):
        """Test the page_items function with an empty list"""
        items: list[str] = []
        items_per_page: int = 3

        result_kb, page = msgs._page_items(items, items_per_page, 0)

        self.assertEqual(result_kb, [[], ["X"]])
        self.assertEqual(page, 0)

    def test_page_items_list_with_one_item(self):
        """Test the page_items function with a list with one item"""
        items: list[str] = ["item1"]
        items_per_page: int = 3

        result_kb, page = msgs._page_items(items, items_per_page, 0)

        self.assertEqual(result_kb, [["item1"], ["X"]])
        self.assertEqual(page, 0)

    def test_page_items_with_one_page(self):
        """Test the page_items function with a list with one page"""
        items: list[str] = ["item1", "item2", "item3"]
        items_per_page: int = 3

        result_kb, page = msgs._page_items(items, items_per_page, 0)

        self.assertEqual(result_kb, [["item1", "item2", "item3"], ["X"]])
        self.assertEqual(page, 0)

    def test_page_items_with_two_pages(self):
        """Test the page_items function with a list with two pages"""
        items: list[str] = ["item1", "item2", "item3", "item4"]
        items_per_page: int = 3

        result_kb, page = msgs._page_items(items, items_per_page, 0)

        self.assertEqual(result_kb, [["item1", "item2", "item3"], ["X", ">"]])
        self.assertEqual(page, 0)

        result_kb, page = msgs._page_items(items, items_per_page, 1)

        self.assertEqual(result_kb, [["item4"], ["<", "X"]])
        self.assertEqual(page, 1)

    def test_page_items_with_five_pages(self):
        """Test the page_items function with a list with five pages"""
        items: list[str] = [
            "item1",
            "item2",
            "item3",
            "item4",
            "item5",
            "item6",
            "item7",
            "item8",
            "item9",
            "item10",
        ]
        items_per_page: int = 3

        result_kb, page = msgs._page_items(items, items_per_page, 0)
        self.assertEqual(result_kb, [["item1", "item2", "item3"], ["X", ">"]])
        self.assertEqual(page, 0)

        result_kb, page = msgs._page_items(items, items_per_page, 1)
        self.assertEqual(result_kb, [["item4", "item5", "item6"], ["<", "X", ">"]])
        self.assertEqual(page, 1)

        result_kb, page = msgs._page_items(items, items_per_page, 2)
        self.assertEqual(result_kb, [["item7", "item8", "item9"], ["<", "X", ">"]])
        self.assertEqual(page, 2)

        result_kb, page = msgs._page_items(items, items_per_page, 3)
        self.assertEqual(result_kb, [["item10"], ["<", "X"]])
        self.assertEqual(page, 3)

    def test_pg_text_inline_keyboard_(self):
        """Test the pg_text_inline_keyboard function"""
        sender: str = "sender"
        items: list[str] = ["item1", "item2", "item3", "item4"]
        max_line_blocks: int = 3
        page: int = 0

        result = msgs.pg_text_inline_keyboard(sender,
                                              items,
                                              max_line_blocks,
                                              page)

        self.assertIsInstance(result, msgs.InlineKeyboardMarkup)

        self.assertEqual(len(result.inline_keyboard), 2)
        self.assertEqual(len(result.inline_keyboard[0]), 3)
        self.assertEqual(len(result.inline_keyboard[1]), 2)

        self.assertEqual(result.inline_keyboard[0][0].text, "item1")
        self.assertEqual(result.inline_keyboard[0][1].text, "item2")
        self.assertEqual(result.inline_keyboard[0][2].text, "item3")
        self.assertEqual(result.inline_keyboard[1][0].text, "X")
        self.assertEqual(result.inline_keyboard[1][1].text, ">")

        result = msgs.pg_text_inline_keyboard(sender,
                                              items,
                                              max_line_blocks,
                                              page + 1)

        self.assertEqual(len(result.inline_keyboard), 2)
        self.assertEqual(len(result.inline_keyboard[0]), 1)
        self.assertEqual(len(result.inline_keyboard[1]), 2)

        self.assertEqual(result.inline_keyboard[0][0].text, "item4")
        self.assertEqual(result.inline_keyboard[1][0].text, "<")
        self.assertEqual(result.inline_keyboard[1][1].text, "X")

    def test_pg_text_inline_keyboard_ask_wrong_page(self):
        """Test the pg_text_inline_keyboard function when asking for a wrong
        page"""
        sender: str = "sender"
        items: list[str] = ["item1", "item2", "item3", "item4"]
        max_line_blocks: int = 3
        page: int = 5

        result = msgs.pg_text_inline_keyboard(sender,
                                              items,
                                              max_line_blocks,
                                              page)

        self.assertIsInstance(result, msgs.InlineKeyboardMarkup)

        self.assertEqual(len(result.inline_keyboard), 2)
        self.assertEqual(len(result.inline_keyboard[0]), 1)
        self.assertEqual(len(result.inline_keyboard[1]), 2)

        self.assertEqual(result.inline_keyboard[1][0].text, "<")
        self.assertEqual(result.inline_keyboard[1][1].text, "X")

        page = -1
        result = msgs.pg_text_inline_keyboard(sender,
                                              items,
                                              max_line_blocks,
                                              page)

        self.assertIsInstance(result, msgs.InlineKeyboardMarkup)

        self.assertEqual(len(result.inline_keyboard), 2)
        self.assertEqual(len(result.inline_keyboard[0]), 3)
        self.assertEqual(len(result.inline_keyboard[1]), 2)

        self.assertEqual(result.inline_keyboard[0][0].text, "item1")
        self.assertEqual(
            result.inline_keyboard[0][0].callback_data,
            "sender:0:0"
        )
        self.assertEqual(result.inline_keyboard[0][1].text, "item2")
        self.assertEqual(
            result.inline_keyboard[0][1].callback_data,
            "sender:1:0"
        )
        self.assertEqual(result.inline_keyboard[0][2].text, "item3")
        self.assertEqual(
            result.inline_keyboard[0][2].callback_data,
            "sender:2:0"
        )

        self.assertEqual(result.inline_keyboard[1][0].text, "X")
        self.assertEqual(result.inline_keyboard[1][1].text, ">")


if __name__ == "__main__":
    unittest.main()
