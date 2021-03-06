from os import environ, path
from functools import lru_cache
from enum import Enum, unique

try:
    from enum import auto
except ImportError:
    _number_auto = 0

    def auto():
        global _number_auto
        _number_auto += 1
        return _number_auto

from . import tl
from .users import Users

TOKEN = environ.get("TL_CRYPTO_BOT")
USERS = Users(path.join(path.dirname(__file__), "..", "data", "users.json"))
SECRET_CODE = "3561"


@lru_cache(maxsize=10)
def updater(token):
    return tl.Updater(token=token)


def get_bot_information():
    bot_ = tl.Bot(token=TOKEN)
    return bot_.get_me()


class StrEnum(Enum):
    def lower(self):
        return self.name.lower()


@unique
class CommandEnum(StrEnum):
    START = auto()
    CHOOSE_INDEX = auto()
    CHOOSE_EXCHANGE = auto()
    UNSUBSCRIBE = auto()

    def command(self):
        return "/" + self.lower()


@unique
class WorkflowEnum(StrEnum):
    CHECK_SECRET_CODE = auto()
    CHOOSE_EXCHANGE = auto()
    CHOOSE_INDEX = auto()
    RECEIVE_INDEX = auto()
    GET_KRAKEN_API = auto()
    UPDATE_KRAKEN_API = auto()
    DONE = auto()


@unique
class UserInfoEnum(StrEnum):
    API_KEY = auto()
    NAME = auto()
    USER_ID = auto()
    INDEX = auto()
    EXCHANGE = auto()
    ACTIVE = auto()


def build_menu(buttons, n_cols=1, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
