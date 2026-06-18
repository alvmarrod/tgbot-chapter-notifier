import os
from typing import Any

try:
    from src.utils import log
    from src.app.messages import load_lang_dict
    from src.app.database import Database
    from src.infrastructure.broker import BrokerConfig
except ModuleNotFoundError:
    from utils import log
    from app.messages import load_lang_dict
    from app.database import Database
    from infrastructure.broker import BrokerConfig

from dotenv import load_dotenv
if os.getenv("TB_CHAPTER_NOTIFIER_TEST", "True") == "True":
    load_dotenv("src/.env_test")
else:
    load_dotenv()

BOT_ID: str = os.getenv("BOT_ID", "chaptnotifier")
SUBSCRIBER_ID: str = os.getenv("SUBSCRIBER_ID", "svc_chaptnotifier")
INCOMING_ROUTING_KEY: str = os.getenv(
    "INCOMING_ROUTING_KEY", f"incoming.events.{BOT_ID}.#"
)
ERROR_QUEUE: str = "chaptnotifier.delivery.errors"

broker_config: BrokerConfig = BrokerConfig.from_env()

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

BOT_COMMANDS: list[dict[str, str]] = [
    {"command": "start", "description": "Start the bot"},
    {"command": "add", "description": "Subscribe to a manga"},
    {"command": "del", "description": "Unsubscribe from a manga"},
    {"command": "list", "description": "List the suscribed mangas"},
]
