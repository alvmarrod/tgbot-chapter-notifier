#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class Chapter:

    def __init__(self, title="", number=0, link=""):
        self.title = title
        self.number = number
        self.link = link

class MangaPandaItem:

    def __init__(self, title="",):
        self.title = title
        self.hour = "recent"
        self.chapters = []

    def setHour(self, hour="recent"):
        self.hour = hour

    def addChapter(self, title, number, link):
        self.chapters.append(Chapter(title, number, link))

    """
    def printAll(self):

        print "\n" + self.title + " - " + self.hour
        for item in self.chapters:
            print "#" + item.number + " - " + item.title + " - " + item.link
    """