from functools import wraps

from . import tl
from . import utils

CMD = utils.CommandEnum
WF = utils.WorkflowEnum


def main_menu():
    command_buttons = [
        tl.KeyboardButton(CMD.START.command()),
        tl.KeyboardButton(CMD.START.command()),
        tl.KeyboardButton(CMD.START.command()),
    ]

    return tl.ReplyKeyboardMarkup(
        utils.build_menu(command_buttons, n_cols=3), resize_keyboard=True
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
                text="Sorry, you need to register first with an invitation "
                     "code."
            )
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def start(bot, update):
    msg = "Hi {}, welcome to use our trading bot!".format(
        update.message.from_user.name
    )
    if update.effective_user.id not in utils.ALL_USERS:
        msg += (" You can first register with an invitation code. "
                "Enter the code")
        update.message.reply_text(msg)
        return WF.RECEIVE_INFO
    else:
        update.message.reply_text(msg)


def register(bot, update):
    code = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id, text=code
    )
    user_id = update.effective_user.id
    if code == utils.SECRET_CODE:
        utils.ALL_USERS.add(user_id)
        with open(utils.USERS_FILENAME, "a") as f_:
            f_.write("\n{}".format(user_id))
        text = "Registration successful! :)"
    else:
        text = "Sorry, the registration code is wrong :("
    bot.send_message(
        chat_id=update.message.chat_id, text=text
    )


def workflow_handler():
    return tl.ConversationHandler(
        entry_points=[tl.CommandHandler(CMD.START.text(), start)],
        states={
            WF.RECEIVE_INFO: [
                tl.MessageHandler(tl.Filters.text, register)
            ],
        },
        fallbacks=[tl.CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
