import logging
import time
import telegram
from telegram.ext import (
    CommandHandler, MessageHandler, Filters, InlineQueryHandler,
)
from telegram import (
    InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton,
    InlineKeyboardMarkup
)

from . import tl
from . import utils
from . import register

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

utils.print_bot_information()

updater = utils.updater(token=utils.TOKEN)
dispatcher = updater.dispatcher


def echo(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text=update.message.text
    )


@register.restricted
def caps(bot, update, args):
    chat_id = update.message.chat_id
    if len(args) >= 2:
        bot.send_chat_action(
            chat_id=chat_id, action=telegram.ChatAction.TYPING
        )
        time.sleep(3)
    text = " ".join(args).upper()
    bot.send_message(
        chat_id=update.message.chat_id, text=text
    )


def nice_caps(bot, update, args):
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id,
        text="*{}* _italic_ `fixed width font` [link](http://google.com)"
             "".format(" ".join(args).upper()),
        parse_mode=telegram.ParseMode.MARKDOWN)


def request_location(bot, update):
    location_keyboard = telegram.KeyboardButton(
        text="send_location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(
        text="send_contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Would you mind sharing your location and contact with me?",
        reply_markup=reply_markup
    )


def inline_caps(bot, update):
    query = update.inline.query
    if not query:
        return
    result = [
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper())
        ),
    ]
    bot.answer_inline_query(update.inline_query.id, result)


def _print(bot, update, chat_data):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Would you mind {}".format(chat_data)
    )


def buttons_show(bot, update):
    button_list = [
        InlineKeyboardButton("col1", callback_data=_print),
        InlineKeyboardButton("col2", callback_data=_print),
        InlineKeyboardButton("row 2", callback_data=_print)
    ]
    reply_markup = InlineKeyboardMarkup(
        utils.build_menu(button_list, n_cols=2)
    )
    bot.send_message(
        chat_id=update.message.chat_id,
        text="A two-column menu", reply_markup=reply_markup
    )


dispatcher.add_handler(register.workflow_handler())
dispatcher.add_handler(MessageHandler(Filters.command, register.unknown))


dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
dispatcher.add_handler(CommandHandler('nice_caps', nice_caps, pass_args=True))
dispatcher.add_handler(CommandHandler('request', request_location))

dispatcher.add_handler(InlineQueryHandler(inline_caps))

updater.start_polling()
updater.idle()
