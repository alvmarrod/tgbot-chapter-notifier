
from typing import Awaitable, Callable

try:
    from src.utils import log
    from src.app.actions import explore_web, process_reporting, prune_suscriptions
    import src.domain.communications as comms
except ModuleNotFoundError:
    from utils import log
    from app.actions import explore_web, process_reporting, prune_suscriptions
    import domain.communications as comms


###############################################################################
#                                  CRON TASKS                                 #
###############################################################################

def perform_search_generator() -> Callable[[], Awaitable[None]]:
    """Returns a function that will:
    1. Search for the mangas scheduled in any chat
    2. Notifies the suscribed chats about the new content
    """

    url: str = "https://mangapanda.onl"

    async def perform_search() -> None:
        """Scrapes the web and notifies the suscribers
        """
        log("bot", "info", ["perform_search", "Searching for new content"])
        explore_web(url)
        report_results: list[tuple[comms.Suscription, Exception]] = \
            await process_reporting()

        prune_suscriptions(report_results)

    return perform_search
