"""Module in charge to define the model to represent the objects required for
user communication in the app"""
from typing import Optional
from dataclasses import dataclass

try:
    from src.utils import log
    from src.domain.model import Manga
    from src.domain.domain_exception import DomainException
except ModuleNotFoundError:
    from utils import log
    from domain.model import Manga
    from domain.domain_exception import DomainException


@dataclass
class Chat():
    """Models a chat that has some suscription for the bot.

    - ID of the chat
    - Name or title of the chat
    """
    id:     int
    name:   str


@dataclass
class Suscription():
    """Models a suscription that someone has performed for some manga at a
    specific chat.

    - Chat ID
    - Manga ID
    - Last chapter been notified

    All are external keys IDs
    """
    chat:   Chat
    manga:  Manga
    last:   str


def search_chat_by_id(chats: list[Chat], target_chat: Chat) -> Optional[Chat]:
    """Searchs the manga list by provided ID"""
    item: Optional[Chat] = None
    for chat in chats:
        if chat.id == target_chat.id:
            item = chat
            break

    return item


def search_suscriptions_by_chat_id(susc: list[Suscription],
                                   chat: Chat) -> list[Suscription]:
    """Searchs the suscription list by provided chat ID"""
    items: list[Suscription] = []
    for sus in susc:
        if sus.chat.id == chat.id:
            items.append(sus)

    return items


def search_suscriptions_by_manga(susc: list[Suscription],
                                 manga: Manga) -> list[Suscription]:
    """Searchs for any suscription for the given manga name"""
    tracking_subs: list[Suscription] = []

    for sus in susc:
        if sus.manga.name == manga.name:
            tracking_subs.append(sus)

    return tracking_subs


# TODO: check if used and delete, as this replicates the same functionality
# implemented in handlers
def add_chat(chats: list[Chat], chat: Chat) -> bool:
    """Adds a new chat to the system"""
    created: bool = False

    try:
        if chats is None or chat is None or \
                chat.id is None or chat.id == 0:
            raise DomainException("Chat ID and name are required")

        if search_chat_by_id(chats, chat) is not None:
            raise DomainException("Chat already exists")

        chats.append(chat)
        created = True

    except DomainException as err:
        log("bot", "err", ["add_chat", " Couldn't add chat"])
        log("bot", "debug", ["add_chat", f" {str(err)}"])
    except Exception as err:
        log("bot", "err", ["add_chat", " Couldn't add chat"])
        log("bot", "debug", ["add_chat", f" {str(err)}"])

    return created


# TODO: check if used and delete, as this replicates the same functionality
# implemented in handlers
def del_chat(chats: list[Chat], chat: Chat) -> bool:
    """Removes a chat from the system"""
    deleted: bool = False

    try:
        if chat is None or chat.id is None or chat.id == 0:
            raise DomainException("Target chat ID is required")

        target_chat: Optional[Chat] = search_chat_by_id(chats, chat)

        if target_chat is None:
            raise DomainException("Chat not found")

        chats.remove(target_chat)
        deleted = True

    except DomainException as err:
        log("bot", "err", ["del_chat", " Couldn't delete chat"])
        log("bot", "debug", ["del_chat", f" {str(err)}"])
    except Exception as err:
        log("bot", "err", ["del_chat", " Couldn't delete chat"])
        log("bot", "debug", ["del_chat", f" {str(err)}"])

    return deleted


# TODO: check if used and delete, as this replicates the same functionality
# implemented in handlers
def add_suscription(susc: list[Suscription], chat: Chat, manga: Manga) -> bool:
    """Adds a suscription to the system"""
    created: bool = False

    try:

        if chat is None or chat.id is None or chat.id == 0:
            raise DomainException("Chat ID is required")
        elif manga is None or manga.name == "":
            raise DomainException("Manga name are required")

        subs: list[Suscription] = search_suscriptions_by_chat_id(susc, chat)
        for sus in subs:
            if sus.manga.name == manga.name:
                raise DomainException("This suscription already exists")

        susc.append(Suscription(chat, manga, ""))
        created = True

    except DomainException as err:
        log("bot", "err", ["add_suscription", " Couldn't add suscription"])
        log("bot", "debug", ["add_suscription", f" {str(err)}"])
    except Exception as err:
        log("bot", "err", ["add_suscription", " Couldn't add suscription"])
        log("bot", "debug", ["add_suscription", f" {str(err)}"])

    return created


# TODO: check if used and delete, as this replicates the same functionality
# implemented in handlers
def del_suscription(sucs: list[Suscription], chat: Chat, manga: Manga) -> bool:
    """Removes a suscription from the system"""
    deleted: bool = False

    try:

        if chat is None or chat.id == 0:
            raise DomainException("Chat ID is required")
        elif manga is None or manga.name == "":
            raise DomainException("Manga name are required")

        target_suscription: Optional[Suscription] = None
        for sus in sucs:
            if sus.chat.id == chat.id and sus.manga.name == manga.name:
                target_suscription = sus
                break

        if target_suscription is None:
            raise DomainException("Couldn't find suscription")

        sucs.remove(target_suscription)
        deleted = True

    except DomainException as err:
        log("bot", "err", ["del_suscription", " Couldn't remove suscription"])
        log("bot", "debug", ["del_suscription", f" {str(err)}"])
    except Exception as err:
        log("bot", "err", ["del_suscription", " Couldn't remove suscription"])
        log("bot", "debug", ["del_suscription", f" {str(err)}"])

    return deleted
