# Chapter Availability Notifier
# Started on Nov 2018

from enum import Enum

import logging
import threading

from emoji import emojize
from functools import wraps

from telegram import ParseMode
from telegram import ChatAction

from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler, MessageHandler

#from Classes.UserBotState import UserBotState
from Classes.ChapterSeeker import ChapterSeeker

# Icons
info_icon = emojize(":information_source: ", use_aliases=True)
ok_icon = emojize(":white_check_mark:", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

bot_icon = emojize(":computer:", use_aliases=True)
user_icon = emojize(":bust_in_silhouette:", use_aliases=True)

exc_icon = emojize(":exclamation: ", use_aliases=True)

# Texts to user

welcome = ["¡Bienvenido al bot Chapter Notifier!\n\n",
" Este bot sirve para estar al tanto de tus mangas favoritos. Para ello, usamos la web MangaPanda.onl\n\n",
" Usa el comando /help para consultar todos los comandos disponibles en este bot"""] #\n\n" ,
#" Dime, ¿qué mangas quieres seguir? Recuerda decirmelos de uno en uno, y cuando acabes usa /done\n\n"]

add_usage = [exc_icon, " Por favor, use:\n\n",
            "/add Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo de la web!"]

add_msg = [info_icon, " Manga añadido a la colección."]
add_error = [error_icon, " ¡El manga ya existe en la colección!"]

del_usage = [exc_icon, " Por favor, use:\n\n",
            "/del Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

del_msg = [info_icon, " Manga eliminado de la colección."]
del_error = [error_icon, " ¡El manga no está en la colección!"]

info_usage = [exc_icon, " Por favor, use:\n\n",
            "/info Nombre del manga\n",
            "Para evitar errores, se recomienda copiarlo del listado!"]

info_msg = [info_icon, " Manga: "]
info_error = [error_icon, " ¡El manga no está en la colección!"]


list_usage = [exc_icon, " Por favor, use solamente:\n\n",
            "/list\n"]

list_msg = [info_icon, "Tu colección incluye:\n\n"]
list_error = [error_icon, "¡La colección está vacía!"]

unknown_user = [exc_icon, " ¡Comando no reconocido!"]

# Logs Texts - Templates
# Bot log
bot_log = bot_icon + ' Funcion: %s - Mensaje: %s'
# User action (OK, NOK)
user_log = user_icon + ' : "@%s" - Comando: %s - Resultado: %s'

# Definitions

class Bot:

    def __init__(self):

        # Logs
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)

        self.__logger = logging.getLogger(__name__)

        # Library objects
        self.__updater = Updater(token="BotFather_provided_token")
        self.__dp = self.__updater.dispatcher

        self.__seeker = ChapterSeeker(self.__updater, "ChapterNotifier.db")

        # Commands binding + Conversation Handlers
        """
        bot_start_handler = ConversationHandler(

            entry_points=[CommandHandler('start', self.start)],

            states={
                botState.MANGA_RECORDING: [RegexHandler('^(Daily|Weekday Only|Close|/cancel)$', self.alarm_type)],

                botState.RUNNING: [RegexHandler('^([0-2][0-9]:[0-5][0-9]|[0-9]:[0-5][0-9]|/cancel)$', self.hour)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        self.dispatcher.add_handler(bot_start_handler)
        """

        self.__dp.add_handler(CommandHandler('start', self.start, pass_args=False))
        self.__dp.add_handler(CommandHandler('add', self.add, pass_args=True))
        self.__dp.add_handler(CommandHandler('del', self.delete, pass_args=True))
        self.__dp.add_handler(CommandHandler('list', self.list, pass_args=True))
        self.__dp.add_handler(CommandHandler('info', self.info, pass_args=True))
        #self.__dp.add_handler(CommandHandler('done', self.done, pass_args=False))
        self.__dp.add_handler(CommandHandler('help', self.help, pass_args=False))
        self.__dp.add_handler(MessageHandler(Filters.command, self.unknown))

    def run(self):
        self.log("bot", "info", ["run", "RUNNING"])
        t1 = threading.Thread(target=self.__seeker.run)
        t1.start()
        self.__updater.start_polling()
        self.__updater.idle()

    # Auxiliar FUNCTIONS
    def send_action(action):
        """Sends `action` while processing func command."""

        def decorator(func):
            @wraps(func)
            def command_func(*args, **kwargs):
                self, bot, update = args
                bot.send_chat_action(chat_id=update.message.chat_id, action=action)
                func(self, bot, update, **kwargs)
            return command_func

        return decorator

    send_typing_action = send_action(ChatAction.TYPING)
    send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
    send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

    def user_collection(self, name, collection_list):
        for item in collection_list:
            if item.user == name:
                return item

    def log(self, origin, type, args):

        if origin == "user":

            if type == "OK":
                prefix = ok_icon
            else: # type == "NOK"
                prefix = error_icon

            # Both info, user faulires are not critical for the bot itself
            self.__logger.info(prefix + user_log, args[0], args[1], args[2])

        else: # origin = bot

            if type == "info":
                prefix = info_icon
                self.__logger.info(prefix + bot_log, args[0], args[1])

            elif type == "warn":
                prefix = warn_icon
                self.__logger.warn(prefix + bot_log, args[0], args[1])

            elif type == "error":
                prefix = error_icon
                self.__logger.error(prefix + bot_log, args[0], args[1])

            else: # type == "critical"
                prefix = critical_icon
                self.__logger.critical(prefix + bot_log, args[0], args[1])

    # COMMAND FUNCTIONS
    @send_typing_action
    def start(self, bot, update):
        try:
            # Create the user in our data
            user = update.effective_user.username
            self.__seeker.addNewUser(user)
            self.log("user", "OK", [user, "start", "Bot iniciado"])
        except Exception as e:
            self.log("user", "NOK", [user, "start", e])

        bot.send_message(chat_id=update.message.chat_id, text="".join(welcome))

    @send_typing_action
    def help(self, bot, update):
        icon = info_icon
        text = icon + " Comandos disponibles en este bot:\n\n"

        commands = [["",  "*Gestión de los mangas*\n"],
                    ["/add",  "Añade un nuevo manga a la lista de seguimiento"],
                    ["/del",  "Elimina el manga indicado de la lista de seguimiento\n"],
                    ["",  "*Información y comportamiento del bot*\n"],
                    ["/list", "Muestra los mangas en seguimiento"],
                    ["/info", "Muestra la información del manga indicado"],
                    #["/done", "Detiene la entrada de mangas al iniciar el bot"],
                    ["/help", "Muestra este mensaje"]
                    ]

        for command in commands:
            text += command[0] + " " + command[1] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=text,
                            parse_mode=ParseMode.MARKDOWN)

    @send_typing_action
    def add(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(add_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = self.__getMangaName(args)

            try:
                self.__seeker.addMangaSuscription(manga, user, update.message.chat_id)

                bot.send_message(chat_id=update.message.chat_id, text="".join(add_msg))
                self.log("user", "OK", [user, "add", manga + " añadido!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(add_error))
                self.log("user", "NOK", [user, "add", e])

    @send_typing_action
    def delete(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(del_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = self.__getMangaName(args)

            try:
                self.__seeker.delMangaSuscription(manga, user, update.message.chat_id)

                bot.send_message(chat_id=update.message.chat_id, text="".join(del_msg))
                self.log("user", "OK", [user, "delete", manga + " eliminado!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(del_error))
                self.log("user", "NOK", [user, "del", e])

    @send_typing_action
    def info(self, bot, update, args):
        if (len(args) == 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(info_usage))

        else:
            # Previous
            user = update.effective_user.username
            manga = self.__getMangaName(args)

            try:
                # Data work
                data_askedfor = self.__seeker.getInfo(manga, user)
                # Messages
                info_user_msg = "".join(info_msg) + manga + "\n\nÚltimo capítulo: " + str(data_askedfor)
                bot.send_message(chat_id=update.message.chat_id, text=info_user_msg)
                self.log("user", "OK", [user, "info", manga + " consultado!"])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(info_error))
                self.log("user", "NOK", [user, "info", e])

    @send_typing_action
    def list(self, bot, update, args):
        if (len(args) != 0):
            bot.send_message(chat_id=update.message.chat_id, text="".join(list_usage))

        else:
            # Previous
            user = update.effective_user.username

            try:
                # Data work
                myMangas = self.__seeker.getMangasFromUser(user)
                # Messages
                list_user_msg = "".join(list_msg)
                for row in range(len(myMangas)):
                    list_user_msg = list_user_msg + myMangas[row][0] + " - Capítulo: " + str(myMangas[row][1]) + "\n"
                bot.send_message(chat_id=update.message.chat_id, text=list_user_msg)
                self.log("user", "OK", [user, "list", "Colección consultada."])
            except Exception as e:
                bot.send_message(chat_id=update.message.chat_id, text="".join(list_error))
                self.log("user", "NOK", [user, "list", e])

    def unknown(self, bot, update):
        user = update.effective_user.username
        bot.send_message(chat_id=update.message.chat_id, text="".join(unknown_user))
        self.log("user", "NOK", [user, update.message.text, "Comando no existente"])

    def __getMangaName(self, args):
        manga = ""
        for item in args:
            manga += item + " "
        manga.replace("\"", "")
        manga = manga[0:len(manga) - 1]

        return manga

if __name__ == '__main__':

    mybot = Bot()
    mybot.run()
