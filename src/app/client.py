import os
from typing import Any, Union

from pyrogram.client import Client
from pyrogram.types import BotCommand

try:
    from src.utils import log
    from src.app.messages import load_lang_dict
    from src.app.database import Database
except ModuleNotFoundError:
    from utils import log
    from app.messages import load_lang_dict
    from app.database import Database

###############################################################################
#                                   CONSTANTS                                 #
###############################################################################

from dotenv import load_dotenv
if os.getenv("TB_CHAPTER_NOTIFIER_TEST", "True") == "True":
    load_dotenv("src/.env_test")
else:
    load_dotenv()

BOT_NAME: str = os.getenv("BOT_NAME", "ChapterNotifier")

API_ID: int = int(os.getenv("TB_CHAPTER_NOTIFIER_API_ID", -1))
API_HASH: str = os.getenv("TB_CHAPTER_NOTIFIER_API_HASH", "")
BOT_TOKEN: str = os.getenv("TB_CHAPTER_NOTIFIER_BOT_TOKEN", "")

###############################################################################
#                                CLIENT & AUTH                                #
###############################################################################


def _get_authorized_client() -> Client:
    """Get the authorized client to interact with the Telegram API"""
    api_client: Client

    try:
        if API_ID == -1:
            log("bot", "error",
                ["client", "API_ID not set. Please set the API_ID"])
            raise AttributeError("API_ID not set")
        api_client = Client(BOT_NAME,
                            api_id=API_ID,
                            api_hash=API_HASH,
                            bot_token=BOT_TOKEN,
                            test_mode=False)

    except AttributeError:
        log("bot", "error",
            ["client",
             "Couldn't create the client. Couldn't authorize bot %s"])
        exit(1)

    return api_client


pyrogram_client: Client = _get_authorized_client()

DATABASE_FILEPATH: str = os.getenv("DATABASE_FILEPATH", "data/roger_db.db")

memory: Database = Database()
log("bot", "info", ["client", f"Starting bot: {DATABASE_FILEPATH}"])
memory.init(DATABASE_FILEPATH)

LANG: str = os.getenv("LANGUAGE", "es_ES")
LANG_DICT: Any

try:
    LANG_DICT = load_lang_dict(LANG)
except FileNotFoundError as e:
    log("bot", "error", ["client.py", str(e)])
    exit(1)

###############################################################################
#                                    COMMANDS                                 #
###############################################################################

# TODO: search, delete_account, help
BOT_COMMANDS: list[dict[str, Union[str, int]]] = [
    {
        "command": "start",
        "description": "Start the bot",
        "group_name": "General",
        "index": 0
    },
    {
        "command": "add",
        "description": "Subscribe to a manga",
        "group_name": "Manga",
        "index": 0
    },
    {
        "command": "del",
        "description": "Unsubscribe from a manga",
        "group_name": "Manga",
        "index": 1
    },
    {
        "command": "list",
        "description": "List the suscribed mangas",
        "group_name": "Manga",
        "index": 2
    }
]


async def set_commands() -> None:
    """Set the commands for the bot"""

    try:
        cmds: list[BotCommand] = []
        for command in BOT_COMMANDS:
            cmds.append(
                BotCommand(
                    command=command["command"],  # type: ignore
                    description=command["description"]  # type: ignore
                )
            )

        await pyrogram_client.set_bot_commands(cmds)
        log("bot", "info", ["client", "Commands set"])

    except AttributeError:
        log("bot", "warning",
            ["client", "".join([
                "Couldn't set the commands. ",
                "Please fix the commands dictionary."])])

    except Exception as e:
        log("bot", "error", ["client", f"Couldn't commands: {e}"])
