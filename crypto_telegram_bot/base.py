import os
from functools import lru_cache, wraps

from telegram.ext import Updater

TOKEN = os.environ["TL_CRYPTO_BOT"]
_USERS_FILENAME = os.path.join(
    os.path.dirname(__file__), "..", "data", "users.txt"
)
with open(_USERS_FILENAME, "r") as f:
    ALL_USERS = set(f.readlines())
SECRET_CODE = "3561"


@lru_cache(maxsize=10)
def updater(token):
    return Updater(token=token)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALL_USERS:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Sorry, you need to /register first with a code."
            )
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def register(bot, update, args):
    if len(args) == 1 and args[0] == SECRET_CODE:
        user_id = update.effective_user.id
        ALL_USERS.add(user_id)
        with open(_USERS_FILENAME, "a") as f_:
            f_.write("\n{}".format(user_id))
        text = "Registration successful! :)"
    else:
        text = "Sorry, the registration code is wrong :("
    bot.send_message(
        chat_id=update.message.chat_id, text=text
    )
