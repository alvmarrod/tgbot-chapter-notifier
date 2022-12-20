#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018

from html.parser import HTMLParser
from Classes.MangaPandaItem import MangaPandaItem

# Docs: https://docs.python.org/2.7/library/htmlparser.html?highlight=htmlparser
# Ref: https://stackoverflow.com/questions/6883049/regex-to-extract-urls-from-href-attribute-in-html-with-python
class MParser(HTMLParser):

    def __init__(self, output_list=None):
        HTMLParser.__init__(self)

        self.type = "none"
        self.recording = 0

        self.currentTitle = ""

        self.currentNumber = ""
        self.currentNameIndex = 0
        self.currentName = ""
        self.currentLink = ""

        self.items = []

    def printAll(self):
        for item in self.items:
            item.printAll()

    def handle_starttag(self, tag, attrs):
        if (tag == 'li') and dict(attrs).get("class") == "iqzwK list-group-item":
                self.recording += 1

        if ((tag == 'h4') and (self.recording == 1)):
            self.recording += 1
        elif ((tag == 'a') and (self.recording == 1)) and \
            (dict(attrs).get("class") == "_8Qtbo text-secondary _2euQb"):
            self.recording += 1
            self.currentLink = dict(attrs).get("href")

        if ((tag == "a") and (self.recording == 2)) and \
            (dict(attrs).get("class") == "_31Z6T text-secondary"):
                self.recording += 1
                self.type = "title"
        elif (tag == "small") and (self.recording == 2) and \
             (dict(attrs).get("class") == "_3L1my"):
                self.recording += 1
                self.type = "hour"
        elif ((tag == "span") and (self.recording == 2)) and \
            (dict(attrs).get("class") == "text-secondary _3D1SJ"):
                self.recording += 1
                self.type = "number"
        elif ((tag == "span") and (self.recording == 2)) and \
            (dict(attrs).get("class") == "_2IG5P"):
                self.recording += 1
                self.type = "chapterName"

    def handle_endtag(self, tag):
        if ((tag == 'li') and (self.recording == 1)) or \
            ((tag == 'h4') and (self.recording == 2)) or \
            ((tag == 'a') and (self.recording == 2)) or \
            ((tag == 'a') and (self.recording == 3)) or \
            ((tag == 'small') and (self.recording == 3)) or \
            ((tag == 'span') and (self.recording == 3)):

            if self.currentName != "":
                #print "#" + self.currentNumber + " - " + self.currentName

                self.items[len(self.items)-1].addChapter( \
                    self.currentName, self.currentNumber, \
                    self.currentLink)

                self.currentNameIndex = 0
                self.currentName = ""
                self.currentLink = ""

            if self.currentTitle != "":
                self.items.append(MangaPandaItem(title=self.currentTitle))
                self.currentTitle = ""

            self.recording -= 1

    def handle_data(self, data):
        if self.recording == 3:
            if self.type == "title":
                # New manga
                self.currentTitle += data
            elif self.type == "hour":
                self.items[len(self.items)-1].setHour(data)
            elif self.type == "number":
                if "#" not in data:
                    self.currentNumber = data
            elif self.type == "chapterName":
                if self.currentNameIndex < 2:
                    self.currentNameIndex += 1
                else:
                    self.currentName += data
            else:
                pass