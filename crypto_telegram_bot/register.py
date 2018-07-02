from functools import wraps

from . import tl
from . import utils

CMD = utils.CommandEnum
WF = utils.WorkflowEnum


def main_menu():
    command_buttons = [
        tl.KeyboardButton(CMD.CHOOSE_INDEX.command()),
        tl.KeyboardButton(CMD.CHOOSE_EXCHANGE.command()),
    ]

    return tl.ReplyKeyboardMarkup(
        utils.build_menu(command_buttons, n_cols=1), resize_keyboard=True
    )


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in utils.USERS:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Sorry, you need to signup first with an invitation "
                     "code. Please enter the invitation code"
            )
            return WF.CHECK_SECRET_CODE
        return func(bot, update, *args, **kwargs)
    return wrapped


def start(bot, update):
    msg = "Hi {}, welcome to our trading bot!".format(
        update.message.from_user.name
    )
    user_id = str(update.effective_user.id)
    if user_id not in utils.USERS or user_id == "590081078":
        msg += (" You can first signup with an invitation code. "
                "Please enter the code")
        update.message.reply_text(msg)
        return WF.CHECK_SECRET_CODE
    else:
        update.message.reply_text(msg, reply_markup=main_menu())
        return tl.ConversationHandler.END


def check_secret_code(bot, update):
    code = update.message.text
    user_id = update.effective_user.id
    if code == utils.SECRET_CODE:
        utils.USERS.add(user_id)
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


def done(bot, update):
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
            WF.CHECK_SECRET_CODE: [
                tl.MessageHandler(tl.Filters.text, check_secret_code)
            ],
            WF.RECEIVE_INDEX: [
                tl.RegexHandler(
                    '^(CRC3|MinMax BTC,ETH|MinMax BTC,ETH,XLM)$',
                    receive_index
                ),
            ],
            WF.CHOOSE_EXCHANGE: [
                tl.RegexHandler('^(kraken)$', choose_exchange),
            ],
            WF.GET_KRAKEN_API: [
                tl.MessageHandler(tl.Filters.text, get_kraken_api)
            ],
        },
        fallbacks=[tl.RegexHandler('^Done$', done)],
        allow_reentry=True
    )


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command. :(",
        reply_markup=main_menu()
    )
