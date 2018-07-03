from os import environ
import logging
import datetime

from . import tl
from . import utils
from . import register
from . import daily

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    app_name = "crypto-telegram-bot"
    logging.info(utils.get_bot_information())
    updater = utils.updater(token=utils.TOKEN)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(environ.get("PORT", "8443")),
                          url_path=utils.TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(
        app_name, utils.TOKEN
    ))

    dp = updater.dispatcher
    dp.add_handler(register.workflow_handler())
    dp.add_handler(tl.MessageHandler(tl.Filters.command, register.unknown))
    dp.add_handler(tl.CommandHandler(
        utils.CommandEnum.UNSUBSCRIBE.command(), register.unsubscribe))

    jq = updater.job_queue
    jq.run_daily(
        daily.push_daily_suggested_order, time=datetime.time(15, 17),
        days=tuple(range(5))
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
