import logging
from typing import List, Any

from emoji import emojize  # type: ignore

################################################################################
#                                    LOGGING                                   #
################################################################################

logging.getLogger("apscheduler").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Icons
DEBUG_ICON: str = emojize(":desktop_computer:")
INFO_ICON: str = emojize(":information:")
OK_ICON: str = emojize(":check_mark_button:")
WARN_ICON: str = emojize(":warning:")
ERROR_ICON: str = emojize(":red_circle:")
CRITICAL_ICON: str = emojize(":black_circle:")

BOT_ICON: str = emojize(":desktop_computer:")
USER_ICON: str = emojize(":bust_in_silhouette:")

EXC_ICON: str = emojize(":exclamation:")

# Logs Texts - Templates
# Bot log
BOT_LOG: str = BOT_ICON + ' Func: %s - Msg: %s'
# User action (OK, NOK)
USER_LOG: str = USER_ICON + ' : "@%s" - Cmd: %s - Result: %s'


def log(origin: str, msg_type: str, args: List[Any]):
    """Logs anything with appropriate icon and format"""

    if origin == "user":

        if msg_type == "OK":
            prefix = OK_ICON
        else:  # msg_type == "NOK"
            prefix = ERROR_ICON

        # Both info, user faulires are not critical for the bot itself
        logging.info(prefix + USER_LOG, args[0], args[1], args[2])

    else:  # origin = bot

        if msg_type == "debug":
            prefix = DEBUG_ICON
            logging.debug(prefix + BOT_LOG, args[0], args[1])

        elif msg_type == "info":
            prefix = INFO_ICON
            logging.info(prefix + BOT_LOG, args[0], args[1])

        elif msg_type == "warn" or msg_type == "warning":
            prefix = WARN_ICON
            logging.warning(prefix + BOT_LOG, args[0], args[1])

        elif msg_type == "error":
            prefix = ERROR_ICON
            logging.error(prefix + BOT_LOG, args[0], args[1])

        else:  # msg_type == "critical"
            prefix = CRITICAL_ICON
            logging.critical(prefix + BOT_LOG, args[0], args[1])


# Icons for interface
LAST_ICON: str = emojize(":left_arrow:")
CALENDAR_ICON: str = emojize(":calendar:")
LINK_ICON: str = emojize(":link:")
NEW_ICON: str = emojize(":NEW_button:")
