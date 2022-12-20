"""Defines all the functions to manage endpoints from bot v1 API"""

from functools import wraps
from typing import Optional

import app.log as lg
from telegram import Update, constants
from telegram.ext import ContextTypes

##############################################################################
###                              Auxiliar Functions                        ###
##############################################################################
def send_action(action: constants.ChatAction):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func

    return decorator

# Define decorators for sending actions
send_typing_action = send_action(constants.ChatAction.TYPING)
send_upload_video_action = send_action(constants.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(constants.ChatAction.UPLOAD_PHOTO)

##############################################################################
###                               Text Constants                           ###
##############################################################################
WELCOME = ["¡Bienvenido al bot Chapter Notifier!\n\n",
"Este bot sirve para estar al tanto de tus mangas favoritos. ",
"Para ello, usamos la web mangapanda.onl\n\n",
"Usa /help para consultar todos los comandos disponibles"""]

UNKNOWN_CMD = [lg.EXC_ICON, "¡Comando no reconocido! Utiliza /help para ver los existentes"]

##############################################################################
###                               Text Constants                           ###
##############################################################################

@send_typing_action
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome function for the user"""

    # User or group
    initializer: Optional[str] = update.message.chat.title
    if not initializer and update.effective_user:
        initializer = update.effective_user.username

    try:
        # self.__seeker.addNewUser(user)

        lg.log("user", "OK", [initializer, "cmd_start", "Bot iniciado"])
    
    except Exception as err:
        lg.log("user", "NOK", [initializer, "cmd_start", err])

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="".join(WELCOME)
    )

@send_typing_action
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to manage the /help command in the bot"""
    # User or group
    initializer: Optional[str] = update.message.chat.title
    if not initializer and update.effective_user:
        initializer = update.effective_user.username
    
    icon = lg.INFO_ICON
    text = icon + "Comandos disponibles en este bot:\n\n"

    commands = [["",  "*Gestión de los mangas*\n"],
                [r"/add \<nombre\>",  "Añade un nuevo manga a tu lista de seguimiento"],
                [r"/del \<nombre\>",  "Elimina el manga indicado de la lista de seguimiento\n"],
                ["",  "*Información y comportamiento del bot*\n"],
                ["/list", "Muestra los mangas en seguimiento"],
                [r"/info \<nombre\>", "Muestra la información del manga indicado"],
                #["/done", "Detiene la entrada de mangas al iniciar el bot"],
                ["/help", "Muestra este mensaje"]
                ]

    for command in commands:
        text += command[0] + " " + command[1] + "\n"

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

    lg.log("user", "OK", [initializer, "cmd_help", "Ayuda mostrada"])

@send_typing_action
async def cmd_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to manage when receiving a command that is not implemented"""
    # User or group
    initializer: Optional[str] = update.message.chat.title
    if not initializer and update.effective_user:
        initializer = update.effective_user.username

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="".join(UNKNOWN_CMD)
    )

    lg.log("user", "NOK", [initializer, update.message.text, "Comando no existente"])
