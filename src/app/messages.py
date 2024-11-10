import os
import json
from typing import Any

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

try:
    from src.utils import log
except ModuleNotFoundError:
    from utils import log

if os.getenv("TB_CHAPTER_NOTIFIER_TEST", "False") == "True" or \
        os.getcwd().endswith("tgbot-chapter-notifier"):
    MODULE_PATH: str = os.getcwd() + os.sep + "src" + os.sep
else:
    MODULE_PATH: str = os.getcwd()

###############################################################################
#                                 AUX FUNCTIONS                               #
###############################################################################


def _page_items(items: list[str], page_items: int, page: int) \
        -> tuple[list[list[str]], int]:
    """Return the items for the given page plus a row of buttons if needed,
    plus the actual page being rendered"""
    actual_pg: int = page
    if page < 0:
        actual_pg = 0
        log("bot", "warn", ["_page_items", "Negative page number: set to 0"])

    start: int = min(
        max(0, actual_pg) * page_items,
        len(items) // page_items * page_items
    )
    end: int = min(start + page_items, len(items))

    # Update actual page
    actual_pg = start // page_items

    if actual_pg == 0 and end == len(items):
        return [items, ["X"]], actual_pg
    elif actual_pg == 0:
        return [items[start:end], ["X", ">"]], actual_pg
    elif actual_pg > 0 and end == len(items):
        return [items[start:end], ["<", "X"]], actual_pg
    else:
        return [items[start:end], ["<", "X", ">"]], actual_pg

###############################################################################
#                                    PUBLIC                                   #
###############################################################################


def load_lang_dict(lang: str) -> Any:
    """Load the language dictionary"""
    language_file: str = os.path.join(MODULE_PATH, f"app/lang/{lang}.json")
    content: Any

    if not os.path.exists(language_file):
        raise FileNotFoundError(
            f"Language file for {lang} not found: {language_file}"
        )

    else:
        content = json.load(open(language_file, "r"))

        for block, cmds in content.items():
            if block == "config":
                continue
            elif block == "generic":
                for generic in cmds.keys():
                    content[block][generic] = "".join(cmds[generic])
            else:
                for cmd, result in cmds.items():
                    for output in result.keys():
                        log(
                            "bot",
                            "debug",
                            [
                                "load_lang_dict",
                                f"{block}{cmd}{output} = {result[output]}"
                            ]
                        )
                        content[block][cmd][output] = "".join(result[output])

    return content


def prepare_message(content: Any) -> str:
    """Prepare the message to be sent to the chat"""
    if isinstance(content, list) and isinstance(content[0], str):
        return "".join(content)
    elif isinstance(content, str):
        return content
    else:
        return " ".join(content)


def pg_get_element_by_position(items: list[str], page: int,
                               position: int,
                               max_line_blocks: int = 3) -> str:
    """Return the element in the given position"""
    items.sort()
    _, actual_pg = _page_items(items, 1, page)
    return items[actual_pg * max_line_blocks + position]


def pg_text_inline_keyboard(source: str,
                            items: list[str],
                            max_line_blocks: int = 3,
                            page: int = 0,
                            ) -> InlineKeyboardMarkup:
    """Prepare the inline keyboard for the message. The source function
    is provided to identify the data source and target."""
    keyboard: list[list[InlineKeyboardButton]] = []

    max_chars: int = 40
    curr_kb: list[list[str]]
    actual_pg: int

    items.sort()
    curr_kb, actual_pg = _page_items(items, max_line_blocks, page)

    for row in curr_kb:
        if any(['>' in row, '<' in row, 'X' in row]):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=button[:min(max_chars, len(button))],
                        callback_data=source + ":"
                        + button + ":" + str(actual_pg)
                    )
                    for button in row
                ]
            )
        else:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=button[:min(max_chars, len(button))],
                        callback_data=source + ":" +
                        str(i) + ":" + str(actual_pg)
                    )
                    for i, button in enumerate(row)
                ]
            )

    return InlineKeyboardMarkup(keyboard)
