import unittest

try:
    import src.infrastructure.web as web
except ModuleNotFoundError:
    import infrastructure.web as web


class TestInfraWeb(unittest.TestCase):
    """Tests for the web infrastructure"""

    def test_download_page_ok(self):
        """Validates that a page can be downloaded"""
        test_url: str = "https://mangapanda.onl"

        html: str = web.download_page(test_url)
        self.assertNotEqual(html, "")

    def test_download_page_nok(self):
        """TODO: Expand into different error codes"""
        wrong_url: str = "https://www.mangapanda.onlfake"

        html: str = web.download_page(wrong_url)
        self.assertEqual(html, "")

    def test_parse_html_ok(self):
        """Validates that a page can be parsed"""
        test_datafile: str = "./tests/data/infra/ok_download_sample.html"

        with open(test_datafile, "r") as file:
            html: str = file.read()

        assert html != "", "Test datafile is empty"

        results: dict[list[dict[str, str]]] = web.parse_html(html)

        # logging.warning(json.dumps(results, indent=4))
        self.assertNotEqual(len(results), 0)

