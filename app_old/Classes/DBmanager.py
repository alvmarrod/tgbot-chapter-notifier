#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018
#
# DB manager class

import sqlite3
import threading

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class DBmanager:

    def __init__(self, file):
        try:
            self.db_con = sqlite3.connect(file, check_same_thread = False)
            self.lock = threading.Lock()
        except Exception as e:
            raise e

    def getAllUsernames(self):
        query_list = ["SELECT name FROM sqlite_master where type = 'table';"]
        askQuery = "".join(query_list)
        try:
            self.lock.acquire()
            result = self.db_con.execute(askQuery).fetchall()
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e
        return result

    def createUserTable(self, user):
        query_list = ["CREATE TABLE ", user,
         " (manga TEXT PRIMARY KEY     NOT NULL,",
         "  chat_id TEXT               NOT NULL);"]
        createQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(createQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def createSeekerTable(self):
        query_list = ["CREATE TABLE Seeker",
         " (manga    TEXT PRIMARY KEY  NOT NULL,",
         "  notified TEXT              NOT NULL);"]
        createQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(createQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def deleteUserTable(self, user):
        query_list = ["DROP TABLE ", user, ";"]
        deleteQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(deleteQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def readUserTable(self, user):
        query_list = ["SELECT * FROM ", user, ";"]
        readQuery = "".join(query_list)
        try:
            self.lock.acquire()
            result = self.db_con.execute(readQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e
        return result

    def addMangaToUser(self, user, manga, chat_id):
        query_list = ["INSERT INTO ", user,
         " (manga, chat_id)",
         "  VALUES (\"",
         manga, "\",\"", str(chat_id), "\");"]
        insertQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(insertQuery)
            self.db_con.commit()
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def delMangaFromUser(self, user, manga, chat_id):
        query_list = ["DELETE from ", user,
         " where manga = \"", manga, "\" AND chat_id = \"",
         str(chat_id), "\";"]
        deleteQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(deleteQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def readMangaFromUser(self, user, manga):
        query_list = ["SELECT * FROM ", user,
         " WHERE manga = \"", manga, "\";"]
        askQuery = "".join(query_list)
        try:
            self.lock.acquire()
            result = self.db_con.execute(askQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e
        return result

    def addMangaToSeeker(self, manga, notified):
        try:
            self.lock.acquire()

            query_list = ["INSERT INTO Seeker (manga, notified) VALUES ",
                            " (\"", manga, "\", \"", notified, "\");" ]
            updateQuery = "".join(query_list)

            self.db_con.execute(updateQuery)
            self.db_con.commit()
            self.lock.release()

        except Exception as e:
            self.lock.release()
            raise e

    def readSeekerTable(self):
        query_list = ["SELECT * FROM Seeker;"]
        readQuery = "".join(query_list)
        try:
            self.lock.acquire()
            result = self.db_con.execute(readQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e
        return result

    def readMangaFromSeeker(self, manga):
        query_list = ["SELECT * FROM Seeker",
         " WHERE manga = \"", manga, "\";"]
        askQuery = "".join(query_list)
        try:
            self.lock.acquire()
            result = self.db_con.execute(askQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e
        return result

    def updateNotifiedFromSeeker(self, manga, notified):
        try:
            self.lock.acquire()

            query_list = ["UPDATE Seeker SET notified = \"", notified, "\"",
                        " WHERE manga = \"", manga, "\";"]
            updateQuery = "".join(query_list)

            self.db_con.execute(updateQuery)
            self.db_con.commit()
            self.lock.release()

        except Exception as e:
            self.lock.release()
            raise e

    def delMangaFromSeeker(self, manga):
        query_list = ["DELETE from Seeker",
         " WHERE manga = \"", manga, "\";" ]
        deleteQuery = "".join(query_list)
        try:
            self.lock.acquire()
            self.db_con.execute(deleteQuery)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def closeDB(self):
        try:
            self.lock.acquire()
            self.db_con.close()
            self.lock.release()
        except Exception as e:
            self.lock.release()