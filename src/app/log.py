"""aaa"""
import logging
from typing import List, Any

from emoji import emojize

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Icons
INFO_ICON = emojize(":information_source: ", use_aliases=True)
OK_ICON = emojize(":white_check_mark:", use_aliases=True)
WARN_ICON = emojize(":warning:", use_aliases=True)
ERROR_ICON = emojize(":red_circle:", use_aliases=True)
CRITICAL_ICON = emojize(":black_circle:", use_aliases=True)

BOT_ICON = emojize(":computer:", use_aliases=True)
USER_ICON = emojize(":bust_in_silhouette:", use_aliases=True)

EXC_ICON = emojize(":exclamation: ", use_aliases=True)

# Texts to user

ADD_USAGE = [EXC_ICON, " Por favor, use:\n\n",
            "/add Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo de la web!"]

ADD_MSG = [INFO_ICON, " Manga añadido a la colección."]
ADD_ERROR = [ERROR_ICON, " ¡El manga ya existe en la colección!"]

DEL_USAGE = [EXC_ICON, " Por favor, use:\n\n",
            "/del Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

DEL_MSG = [INFO_ICON, " Manga eliminado de la colección."]
DEL_ERROR = [ERROR_ICON, " ¡El manga no está en la colección!"]

INFO_USAGE = [EXC_ICON, " Por favor, use:\n\n",
            "/info Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

INFO_MSG = [INFO_ICON, " Manga: "]
INFO_ERROR = [ERROR_ICON, " ¡El manga no está en la colección!"]


LIST_USAGE = [EXC_ICON, " Por favor, use solamente:\n\n",
            "/list\n"]

LIST_MSG = [INFO_ICON, "Tu colección incluye:\n\n"]
LIST_ERROR = [ERROR_ICON, "¡La colección está vacía!"]

# Logs Texts - Templates
# Bot log
BOT_LOG = BOT_ICON + ' Funcion: %s - Mensaje: %s'
# User action (OK, NOK)
USER_LOG = USER_ICON + ' : "@%s" - Comando: %s - Resultado: %s'

def log(origin: str, msg_type: str, args: List[Any]):
    """Logs anything with appropriate icon and format"""

    if origin == "user":

        if msg_type == "OK":
            prefix = OK_ICON
        else: # msg_type == "NOK"
            prefix = ERROR_ICON

        # Both info, user faulires are not critical for the bot itself
        logging.info(prefix + USER_LOG, args[0], args[1], args[2])

    else: # origin = bot

        if msg_type == "info":
            prefix = INFO_ICON
            logging.info(prefix + BOT_LOG, args[0], args[1])

        elif msg_type == "warn":
            prefix = WARN_ICON
            logging.warning(prefix + BOT_LOG, args[0], args[1])

        elif msg_type == "error":
            prefix = ERROR_ICON
            logging.error(prefix + BOT_LOG, args[0], args[1])

        else: # msg_type == "critical"
            prefix = CRITICAL_ICON
            logging.critical(prefix + BOT_LOG, args[0], args[1])
