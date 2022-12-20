#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Naipsas - Btc Sources
# Chapter Availability Notifier
# Started on Nov 2018
#
# userBotState class - Represents the current state of the bot for an user

from enum import Enum

if __name__ == "__main__":
    raise Exception("Este fichero es una clase no ejecutable")

class UserBotState(Enum):
    NONE = 0
    NEW = 1
    MANGA_RECORDING = 2
    RUNNING = 3