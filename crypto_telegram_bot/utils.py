from os import environ, path
from functools import lru_cache
import re
from enum import Enum, auto, unique

from . import tl

TOKEN = environ.get("TL_CRYPTO_BOT")
USERS_FILENAME = path.join(path.dirname(__file__), "..", "data", "users.txt")
with open(USERS_FILENAME, "r") as f:
    ALL_USERS = set(f.readlines())
SECRET_CODE = "3561"


@lru_cache(maxsize=10)
def updater(token):
    return tl.Updater(token=token)


def cancel_button():
    return [tl.KeyboardButton(CommandEnum.CANCEL.command())]


@unique
class CommandEnum(Enum):
    START = auto()
    REGISTER = auto()
    CANCEL = auto()

    def text(self):
        return self.name.replace("_", " ").lower()

    def command(self):
        return "/" + self.name.lower()


@unique
class WorkflowEnum(Enum):
    REGISTER = auto()
    RECEIVE_INFO = auto()


def build_menu(buttons, n_cols=1, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def comp(pattern):
    return re.compile("^" + pattern + "$", re.IGNORECASE)
