from os import environ
import platform
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


def main(is_local):
    logging.info(utils.get_bot_information())
    updater = utils.updater(token=utils.TOKEN)
    if not is_local:
        updater.start_webhook(listen="0.0.0.0",
                              port=int(environ.get("PORT", "8443")),
                              url_path=utils.TOKEN)
        app_name = "crypto-telegram-bot"
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
    main(is_local=platform.node() in {"stars"})
