"""Module in charge to work with the web, retrieving and parsing
the information"""
import urllib.request
from typing import Any, Optional
from bs4 import BeautifulSoup, ResultSet, element

try:
    from src.utils import log
except ModuleNotFoundError:
    from utils import log


def download_page(url: str) -> str:
    """Downloads the page from the given URL and returns the HTML content
    as string"""

    agent_headers: dict[str, str] = {
        'User-Agent': 'Mozilla/5.0'
    }

    html: str = ""
    try:
        req: urllib.request.Request = \
            urllib.request.Request(url, headers=agent_headers)
        with urllib.request.urlopen(req) as response:
            raw_html: bytes = response.read()
            html = raw_html.decode("utf-8")

    except Exception as err:
        log("bot", "error",
            ["download_page", f"Error downloading page: {str(err)}"])

    return html


def parse_html(html: str) -> dict[str, list[dict[str, str]]]:
    """Parses the HTML content and returns the text content"""

    results: dict[str, list[dict[str, str]]] = {}
    try:
        soup = BeautifulSoup(html, "html.parser")

        media: ResultSet[Any]
        for media in soup.find_all("div", class_="media"):
            media_left: ResultSet[Any] = media.find("div", class_="media-left")
            media_body: ResultSet[Any] = media.find("div", class_="media-body")

            if len(media_left) and len(media_body):

                manga_name: str = media_body.find("h4").find_all("a")[0].get_text()
                latest_episode: element.Tag = media_body.find("a", recursive=False)

                episode: Optional[dict[str, str]] = None

                try:
                    episode = {
                        "episode": str(latest_episode.find("span").get_text().strip("#")),
                        "url": str(latest_episode["href"])
                    }
                except AttributeError:
                    log("bot", "debug",
                        ["parse_html",
                         "Reached the list of popular manga. Skipping..."
                         ])
                    break
                finally:
                    if episode:
                        if manga_name not in results:
                            results[manga_name] = []
                        results[manga_name].append(episode)

    except Exception as err:
        log("bot", "error", ["parse_html", f"Error parsing HTML: {str(err)}"])

    return results
