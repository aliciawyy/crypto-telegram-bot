from functools import lru_cache

from telegram.ext import Updater


@lru_cache(maxsize=10)
def updater(token):
    return Updater(token=token)
