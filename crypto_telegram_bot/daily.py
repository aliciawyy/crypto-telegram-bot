from . import utils


def push_daily_suggested_order(bot, job):
    for user_id in utils.USERS.users:
        bot.send_message(int(user_id), "push_daily_suggested_order")