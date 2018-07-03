from functools import wraps

from . import tl
from . import utils

CMD = utils.CommandEnum
WF = utils.WorkflowEnum
UI = utils.UserInfoEnum


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
        update.message.from_user.first_name
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
def receive_index(bot, update, user_data):
    index = update.message.text
    update.message.reply_text(
        'So you would like to follow the index {}! Nice, '
        'now you can choose an exchange to trade'.format(index),
        reply_markup=tl.ReplyKeyboardMarkup(
            [["kraken"]], one_time_keyboard=True
        )
    )
    user_data[UI.INDEX.lower()] = index
    return WF.CHOOSE_EXCHANGE


@restricted
def choose_exchange(bot, update, user_data):
    exchange = update.message.text
    user_data[UI.EXCHANGE.lower()] = exchange
    if exchange != "kraken":
        raise NotImplementedError()
    info = utils.USERS[update.effective_user.id]
    api_keys = info.get(UI.API_KEY.lower())
    if not api_keys:
        update.message.reply_text(
            text="To trade at kraken, you need to share your kraken api with "
                 "me. You can copy paste your api in reply"
        )
        return WF.GET_KRAKEN_API
    else:
        update.message.reply_text(
            text="We have registered your api key {}***{}. Do you want to "
                 "continue to use it?".format(api_keys[:2], api_keys[-2:]),
            reply_markup=tl.ReplyKeyboardMarkup(
                [["Yes", "No"]], one_time_keyboard=True)
        )
        return WF.UPDATE_KRAKEN_API


def update_kraken_api(bot, update, user_data):
    response = update.message.text.lower()
    if response == "yes":
        return done(bot, update, user_data)
    elif response == "no":
        update.message.reply_text(
            "Ok. You can copy paste your new api in reply"
        )
        return WF.GET_KRAKEN_API


def get_kraken_api(bot, update, user_data):
    api_keys = update.message.text
    user_data[UI.API_KEY.lower()] = api_keys
    return done(bot, update, user_data)


def done(bot, update, user_data):
    user_id = update.effective_user.id
    user_data[UI.USER_ID.lower()] = user_id
    user_data[UI.NAME.lower()] = update.message.from_user.name
    utils.USERS.add(user_id, user_data)
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
                    receive_index, pass_user_data=True,
                ),
            ],
            WF.CHOOSE_EXCHANGE: [
                tl.RegexHandler(
                    '^(kraken)$', choose_exchange, pass_user_data=True
                ),
            ],
            WF.UPDATE_KRAKEN_API: [
                tl.RegexHandler(
                    '^(Yes|No)$', update_kraken_api, pass_user_data=True
                ),
            ],
            WF.GET_KRAKEN_API: [
                tl.MessageHandler(
                    tl.Filters.text, get_kraken_api, pass_user_data=True
                )
            ],
        },
        fallbacks=[tl.RegexHandler('^Done$', done, pass_user_data=True)],
        allow_reentry=True
    )


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command. :(",
        reply_markup=main_menu()
    )
