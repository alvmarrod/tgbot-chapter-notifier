from typing import Awaitable, Callable, Optional

try:
    from src.utils import log
    from src.app.actions import explore_web, process_reporting, prune_suscriptions
    import src.domain.communications as comms
    from src.infrastructure.broker import ResponsePublisher
except ModuleNotFoundError:
    from utils import log
    from app.actions import explore_web, process_reporting, prune_suscriptions
    import domain.communications as comms
    from infrastructure.broker import ResponsePublisher


def perform_search_generator(
    publisher: Optional[ResponsePublisher] = None,
    bot_id: str = "",
) -> Callable[[], Awaitable[None]]:
    url: str = "https://mangapanda.onl"

    async def perform_search() -> None:
        log("bot", "info", ["perform_search", "Searching for new content"])
        explore_web(url)
        report_results: list[tuple[comms.Suscription, Exception]] = \
            await process_reporting(publisher, bot_id)

        prune_suscriptions(report_results)

    return perform_search
