import os

import telegram
from telegram.ext import Updater, CommandHandler

import logging
log = logging.getLogger(__name__)

token = os.environ["TL_CRYPTO_BOT"]
bot_ = telegram.Bot(token=token)

print(bot_.get_me())

updater = Updater(token=token)
dispatcher = updater.dispatcher


def hello(bot, update):
    update.message.reply_text(
        "Hello {}{}".format(
            update.message.text.lower(), update.message.from_user.firsname)
    )


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I'm a bot bot, please talk to me!"
    )


dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()

