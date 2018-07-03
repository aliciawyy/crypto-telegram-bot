from . import utils


def push_daily_suggested_order(bot, job):
    for user_id, info in utils.USERS.data.items():
        if bool(info[utils.UserInfoEnum.ACTIVE]):
            bot.send_message(int(user_id), "push_daily_suggested_order")
