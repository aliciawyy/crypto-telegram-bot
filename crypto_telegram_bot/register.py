from functools import wraps

from . import tl
from . import utils

CMD = utils.CommandEnum
WF = utils.WorkflowEnum

signup_option_keyboard = [
    ["Choose Index"],
    ['Number of siblings'],
    ['Done'],
]
signup_option_markup = tl.ReplyKeyboardMarkup(
    signup_option_keyboard, one_time_keyboard=True
)


def main_menu():
    command_buttons = [
        tl.KeyboardButton(CMD.CHOOSE_INDEX.command()),
        tl.KeyboardButton(CMD.CHOOSE_EXCHANGE.command()),
    ]

    return tl.ReplyKeyboardMarkup(
        utils.build_menu(command_buttons, n_cols=1), resize_keyboard=True
    )


def cancel(bot, update, chat_data=None):
    update.message.reply_text("Canceled...", reply_markup=main_menu())
    return tl.ConversationHandler.END


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in utils.ALL_USERS:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Sorry, you need to signup first with an invitation "
                     "code. Please enter the invitation code"
            )
            return WF.SIGNUP
        return func(bot, update, *args, **kwargs)
    return wrapped


def start(bot, update):
    msg = "Hi {}, welcome to our trading bot!".format(
        update.message.from_user.name
    )
    user_id = str(update.effective_user.id)
    if user_id not in utils.ALL_USERS or user_id == "590081078":
        msg += (" You can first signup with an invitation code. "
                "Please enter the code")
        update.message.reply_text(msg)
        return WF.SIGNUP
    else:
        update.message.reply_text(msg, reply_markup=main_menu())
        return tl.ConversationHandler.END


def signup(bot, update):
    code = update.message.text
    user_id = update.effective_user.id
    if code == utils.SECRET_CODE:
        utils.ALL_USERS.add(user_id)
        with open(utils.USERS_FILENAME, "a") as f_:
            f_.write("\n{}".format(user_id))
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Registration successful! :)"
        )
        return choose_index(bot, update)
    else:
        text = "Sorry, the registration code is wrong :("
        bot.send_message(
            chat_id=update.message.chat_id, text=text
        )
        return tl.ConversationHandler.END


@restricted
def choose_index(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="You can choose your favorite crypto index to trade",
        reply_markup=tl.ReplyKeyboardMarkup(
            [["CRC3"], ["MinMax BTC,ETH"], ["MinMax BTC,ETH,XLM"]],
            one_time_keyboard=True
        )
    )
    return WF.RECEIVE_INDEX


@restricted
def choose_exchange(bot, update):
    exchange = update.message.text
    if exchange == "kraken":
        update.message.reply_text(
            'To trade at kraken, you need to share your kraken api with me. '
            'You can copy paste your api in reply'
        )
        return WF.GET_KRAKEN_API
    else:
        raise NotImplementedError()


@restricted
def receive_index(bot, update):
    index = update.message.text
    update.message.reply_text(
        'So you would like to follow the index {}! Nice, '
        'now you can choose an exchange to trade'.format(index),
        reply_markup=tl.ReplyKeyboardMarkup(
                [["kraken"]], one_time_keyboard=True
        )
    )
    return WF.CHOOSE_EXCHANGE


def get_kraken_api(bot, update):
    api_keys = update.message.text
    update.message.reply_text(
        "Nice! Now I have registered your keys {}".format(api_keys),
        reply_markup=main_menu())
    return WF.DONE


def sign_up_end(bot, update):
    update.message.reply_text(
        "Thanks! That's all I need for the signup. See you next time!",
        reply_markup=main_menu())
    return tl.ConversationHandler.END


def workflow_handler():
    return tl.ConversationHandler(
        entry_points=[
            tl.CommandHandler(CMD.START.lower(), start),
            tl.CommandHandler(CMD.CHOOSE_INDEX.lower(), choose_index),
            tl.CommandHandler(CMD.CHOOSE_EXCHANGE.lower(), choose_exchange),
        ],
        states={
            WF.SIGNUP: [
                tl.MessageHandler(tl.Filters.text, signup)
            ],
            WF.RECEIVE_INDEX: [
                tl.RegexHandler(
                    '^(CRC3|MinMax BTC,ETH|MinMax BTC,ETH,XLM)$', receive_index
                ),
            ],
            WF.CHOOSE_EXCHANGE: [
                tl.RegexHandler('^(kraken)$', choose_exchange),
            ],
            WF.GET_KRAKEN_API: [
                tl.MessageHandler(tl.Filters.text, get_kraken_api)
            ],
        },
        fallbacks=[tl.RegexHandler('^Done$', sign_up_end, pass_user_data=True)],
        allow_reentry=True
    )
