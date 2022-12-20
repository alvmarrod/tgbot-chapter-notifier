"""Module to define the bot actions, based on all other modules.

Specially, it would depend on bot_cmds_vX modules"""

from typing import Callable
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Application, filters

import app.log as lg
import app.bot_cmds_v1 as bot_v1

##############################################################################
###                         Public Functions to be Invoked                 ###
##############################################################################
def build_basic_bot(prov_token: str) -> Application:
    """Builds the bot Application object with the provided token and returns it"""
    return ApplicationBuilder().token(prov_token).build()

def add_actions_v1(app: Application):
    """Adds all v1 endpoints to the bot to listen in the appropriate commands"""
    _add_cmd_action(app, 'start', bot_v1.cmd_start)
    _add_cmd_action(app, 'help', bot_v1.cmd_help)
    _add_msg_handler(app, filters.COMMAND, bot_v1.cmd_unknown)

def run_bot(app: Application):
    """Starts and setups the bot application"""
    lg.log("bot", "info", ["run", "RUNNING"])
    app.run_polling()

##############################################################################
###                             Private Functions                          ###
##############################################################################

def _add_cmd_action(app: Application, cmd: str, func: Callable):
    """Adds any given function at the given command to the bot"""
    handler = CommandHandler(cmd, func)
    app.add_handler(handler)

def _add_msg_handler(app: Application, msg_filter: filters.BaseFilter, func: Callable):
    """Adds a given function to manage messages that are collected
    by a given filter"""
    handler = MessageHandler(msg_filter, func)
    app.add_handler(handler)
