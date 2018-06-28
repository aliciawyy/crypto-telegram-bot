import os
from functools import lru_cache, wraps

from . import tl
from . import utils

TOKEN = os.environ["TL_CRYPTO_BOT"]
_USERS_FILENAME = os.path.join(
    os.path.dirname(__file__), "..", "data", "users.txt"
)
with open(_USERS_FILENAME, "r") as f:
    ALL_USERS = set(f.readlines())
SECRET_CODE = "3561"


@lru_cache(maxsize=10)
def updater(token):
    return tl.Updater(token=token)


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


def start(bot, update):
    msg = ("Hi {}, welcome to use our trading bot! You can first register "
           "with the code you received before"
           ".".format(update.message.from_user.name))
    keyboards = tl.ReplyKeyboardMarkup(
        utils.build_menu([tl.KeyboardButton("/register")], n_cols=1),
        resize_keyboard=True)
    update.message.reply_text(msg, reply_markup=keyboards)


def register(bot, update):
    user_id = update.effective_user.id
    if user_id not in ALL_USERS:

        ALL_USERS.add(user_id)
        with open(_USERS_FILENAME, "a") as f_:
            f_.write("\n{}".format(user_id))
        text = "Registration successful! :)"
    else:
        text = "Sorry, the registration code is wrong :("
    bot.send_message(
        chat_id=update.message.chat_id, text=text
    )


def clear_chat_data(chat_data):
    if chat_data:
        for key in list(chat_data.keys()):
            del chat_data[key]


def main_menu():
    reply_msg = "Buy or sell?"

    buttons = [
        tl.KeyboardButton(utils.CommandEnum.START.text()),
        tl.KeyboardButton(utils.CommandEnum.CANCEL.text()),
    ]
    cancel_btn = [
        tl.KeyboardButton(utils.CommandEnum.CANCEL.text())
    ]

    menu = utils.build_menu(buttons, n_cols=2, footer_buttons=cancel_btn)
    reply_mrk = tl.ReplyKeyboardMarkup(menu, resize_keyboard=True)
    update.message.reply_text(reply_msg, reply_markup=reply_mrk)


def cancel(bot, update, chat_data=None):
    update.message.reply_text("Canceled...", reply_markup=main_menu())
    return tl.ConversationHandler.END

"""
trade_handler = tl.ConversationHandler(
    entry_points=[tl.CommandHandler('register', register)],
    states={
        utils.WorkflowEnum.REGISTER:
            [RegexHandler(comp("^(BUY|SELL)$"), trade_buy_sell, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_CURRENCY:
            [RegexHandler(comp("^(" + regex_coin_or() + ")$"), trade_currency, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True),
             RegexHandler(comp("^(ALL)$"), trade_sell_all)],
        WorkflowEnum.TRADE_SELL_ALL_CONFIRM:
            [RegexHandler(comp("^(YES|NO)$"), trade_sell_all_confirm)],
        WorkflowEnum.TRADE_PRICE:
            [RegexHandler(comp("^((?=.*?\d)\d*[.,]?\d*|MARKET PRICE)$"), trade_price, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOL_TYPE:
            [RegexHandler(comp("^(" + regex_asset_or() + ")$"), trade_vol_asset, pass_chat_data=True),
             RegexHandler(comp("^(VOLUME)$"), trade_vol_volume, pass_chat_data=True),
             RegexHandler(comp("^(ALL)$"), trade_vol_all, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOLUME:
            [RegexHandler(comp("^^(?=.*?\d)\d*[.,]?\d*$"), trade_volume, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOLUME_ASSET:
            [RegexHandler(comp("^^(?=.*?\d)\d*[.,]?\d*$"), trade_volume_asset, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_CONFIRM:
            [RegexHandler(comp("^(YES|NO)$"), trade_confirm, pass_chat_data=True)]
    },
    fallbacks=[tl.CommandHandler('cancel', cancel, pass_chat_data=True)],
    allow_reentry=True)
"""