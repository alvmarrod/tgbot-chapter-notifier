"""
Chapter Notifier Telegram Bot

This bot checks for new content on certain websites to notify the user that has
previously suscribed about it.
"""
from pyrogram.sync import idle
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    from src.app.client import (
        pyrogram_client,
        set_commands
    )
    import src.app.handlers  # noqa
    from src.app.cron import perform_search_generator
    from src.utils import log

except ModuleNotFoundError:
    from app.client import (
        pyrogram_client,
        set_commands
    )
    import app.handlers  # noqa
    from app.cron import perform_search_generator
    from utils import log

###############################################################################
#                                     MAIN                                    #
###############################################################################

scheduler = AsyncIOScheduler()
scheduler.start()
scheduler.add_job(perform_search_generator(), "cron", minute="*/15")


async def main():
    """Setup and startup main bot loop"""

    log("bot", "info", ["main", "Starting bot"])
    await pyrogram_client.start()

    log("bot", "info", ["main", "Setting bot commands"])
    await set_commands()

    log("bot", "info", ["main", "Running discovery for init"])
    await perform_search_generator()()

    log("bot", "info", ["main", "Starting polling"])
    await idle()
    await pyrogram_client.stop()

if __name__ == '__main__':
    assert pyrogram_client is not None, "Pyrogram client is None"
    pyrogram_client.run(main())
