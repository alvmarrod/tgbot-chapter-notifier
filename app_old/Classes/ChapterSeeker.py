#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

import time
import logging

import urllib.error
import urllib.request

from emoji import emojize
from telegram import ParseMode

from Classes.MParser import MParser
from Classes.DBmanager import DBmanager
from Classes.SeekedManga import SeekedManga

# Logs Texts - Templates
bot_icon = emojize(":computer:", use_aliases=True)
bot_log = bot_icon + ' ChapterSeeker - Funcion: %s - Mensaje: %s'

ok_icon = emojize(":white_check_mark:", use_aliases=True)
info_icon = emojize(":information_source: ", use_aliases=True)
warn_icon = emojize(":warning:", use_aliases=True)
error_icon = emojize(":red_circle:", use_aliases=True)
critical_icon = emojize(":black_circle:", use_aliases=True)

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class ChapterSeeker:

    def __init__(self, updater, db_file):

        # basicConfig
        self.__sleepTime = 50 # 3600

        # Data. Suscriptors is a list of lists
        self.__mangaList = []
        self.__suscriptors = []

        # We keep the logger, bot and db objects
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                             level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__updater = updater

        # Open DB file and prepare it
        try:
            self.__db = DBmanager(db_file)
            self.__log("info", ["init", "DB Conectada: " + db_file])
        except Exception as e:
            self.__log("critical", ["init", "No se pudo conectar a la base de datos: " + db_file])
            exit()

        try:
            self.__db.createSeekerTable()
            self.__log("info", ["init", "Seeker DB creada"])
        except Exception as e:
            self.__log("info", ["init", "Seeker DB ya existe"])

        # Load data from Database
        try:
            self.__loadSeekerDB()
            self.__loadUsersDB()
        except Exception as e:
            self.__log("error", ["init", "No se pueden cargar los datos de la BD"])
            raise e

    def __log(self, type, args):

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

    def __loadSeekerDB(self):
        mangas_cursor = self.__db.readSeekerTable()
        for manga_item in mangas_cursor:
            # Manga, Latest
            self.__mangaList.append(SeekedManga(manga_item[0], manga_item[1]))


    """
    Cannot use addMangaSuscription cause it's public and uses __addSuscriber
    with default writing to DB
    """
    def __loadUsersDB(self):
        users_cursor = self.__db.getAllUsernames()
        for user_item in users_cursor:
            if user_item[0] != "Seeker":
                user_cursor = self.__db.readUserTable(user_item[0])
                for manga_item in user_cursor:
                    self.__addMangaSuscriptionFromDB(manga_item[0], user_item[0], manga_item[1])

    def __addMangaSuscriptionFromDB(self, manga, user, chat_id):
        try:
            found = False
            index = 0
            for item in self.__mangaList:
                if item.name == manga:
                    found = True
                else:
                    if not found:
                        index += 1

            if found == False:
                self.__mangaList.append(SeekedManga(manga, last))
                self.__db.addMangaToSeeker(manga, last)

            self.__addSuscriber(index, user, chat_id, False)

            self.__log("info", ["__addMangaSuscription", user + " añadido a " + manga])

        except Exception as e:
            # self.__log("info", ["addMangaSuscription", e])
            self.__log("info", ["__addMangaSuscription", user + " ya suscrito a " + manga])
            raise e

    def addNewUser(self, user):
        try:
            self.__db.createUserTable(user)
        except Exception as e:
            raise e

    def addMangaSuscription(self, manga, user, chat_id):
        try:
            found = False
            index = 0
            for item in self.__mangaList:
                if item.name == manga:
                    found = True
                else:
                    if not found:
                        index += 1

            if found == False:
                self.__mangaList.append(SeekedManga(manga, last))
                self.__db.addMangaToSeeker(manga, last)

            self.__addSuscriber(index, user, chat_id)

            self.__log("info", ["addMangaSuscription", user + " añadido a " + manga])

        except Exception as e:
            # self.__log("info", ["addMangaSuscription", e])
            self.__log("info", ["addMangaSuscription", user + " ya suscrito a " + manga])
            raise e

    def __addSuscriber(self, index, user, chat_id, save_to_DB=True):

        if index == len(self.__suscriptors):
            self.__suscriptors.append([])

        # Check if the user already exists
        found = False
        for item in self.__suscriptors[index]:
            if item[0] == user:
                found = True

        if not found:
            self.__suscriptors[index].append([user, chat_id])
            if save_to_DB:
                self.__db.addMangaToUser(user, self.__mangaList[index].name, chat_id)
        else:
            raise Exception(user + " ya suscrito.")

    def delMangaSuscription(self, manga, user, chat_id):
        try:
            found = False
            index = 0
            for item in self.__mangaList:
                if item.name == manga:
                    found = True
                else:
                    if not found:
                        index += 1

            if not found:
                raise Exception("El manga no existe en las suscripciones")
            else:
                self.__delSuscriber(index, user, chat_id)
                # If it's empty already
                if self.__getSuscribersNum(index) == 0:
                    self.__mangaList.remove(item)
                    self.__suscriptors.remove(self.__suscriptors[index])
                    self.__db.delMangaFromSeeker(manga)

        except Exception as e:
            self.__log("info", ["delMangaSuscription", e])
            raise e

    def __delSuscriber(self, index, user, chat_id):

        # Check if the user exists
        found = False
        for manga in self.__suscriptors[index]:
            for item in manga:
                if (item[0] == user) and (item[1] == chat_id):
                    self.__suscriptors[index].remove(item)
                    self.__db.delMangaFromUser(user, self.__mangaList[index].name, chat_id)
                    found = True

        if not found:
            raise Exception(user + " no suscrito.")

    def __getSuscribersNum(self, index):
        return len(self.__suscriptors[index])

    def getInfo(self, manga, user):
        try:
            result = "No está suscrito"
            index = 0

            for item in self.__mangaList:
                if item.name == manga:
                    if self.__checkSuscriber(index, user):
                        result = self.__mangaList[index].last_notified
                index += 1

            return result

        except Exception as e:
            raise e

    def __checkSuscriber(self, index, user):
        found = False
        for manga in self.__suscriptors[index]:
            for item in manga:
                if item == user:
                    found = True

        return found

    def getMangasFromUser(self, user):
        try:
            results = []
            index = 0
            for manga in self.__mangaList:
                if self.__checkSuscriber(index, user):
                    results.append([manga.name, manga.last_notified])
                index += 1

            return results

        except Exception as e:
            raise e

    def __checkManga(self, manga):
        newAvailable = False
        # Check if new chapter is available
        try:

            hdr = {'User-Agent':'Mozilla/5.0'}
            req = urllib.request.Request('https://www.mangapanda.onl/', headers=hdr)

            try:
                page = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                #print(e.fp.read())
                pass

            myParser = MParser()
            myParser.feed(str(page.read()))

            for item in myParser.items:
                if manga.name.lower() in item.title.lower():
                    for chapter in item.chapters:
                        if float(chapter.number) > float(manga.last_notified):
                            manga.last_notified = chapter.number
                            myChapter = chapter
                            newAvailable = True

            page.close()
        except Exception as e:
            #page.close()
            #self.__log("warning", ["checkManga", "No se ha podido conectar con la URL"])
            print(e)

        if newAvailable:
            newChapter = "#" + myChapter.number + " " + myChapter.title
            self.__log("info", ["checkManga", manga.name + " ahora tiene el capítulo:  " + newChapter])
            self.__notifyUsers(manga, newChapter, myChapter.link)
            self.__db.updateNotifiedFromSeeker(manga.name, myChapter.number)

    def __notifyUsers(self, manga, chapter, link):
        self.__log("info", ["notifyUsers", manga.name + " está siendo notificado a los suscriptores!"])

        msg = [ok_icon, " *" + manga.name + " - Capítulo disponible*\n\n",
                manga.name + " - " + "[" + chapter + "](" + link + ")" ]

        for user in self.__suscriptors[self.__getMangaIndex(manga.name)]:
            self.__updater.bot.send_message(chat_id=user[1], text="".join(msg), parse_mode=ParseMode.MARKDOWN)

    def __getMangaIndex(self, manga):
        found = False
        index = 0
        for item in self.__mangaList:
            if item.name == manga:
                found = True
            else:
                if not found:
                    index += 1

        if found:
            return index
        else:
            raise Exception("Manga no encontrado")

    def run(self):

        while (True):

            for manga in self.__mangaList:

                # Look for a new Chapter
                self.__checkManga(manga)

            # After work done, we sleep
            time.sleep(self.__sleepTime)

