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
    logging.info(utils.get_bot_information())
    updater = utils.updater(token=utils.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(register.workflow_handler())
    dp.add_handler(tl.MessageHandler(tl.Filters.command, register.unknown))

    jq = updater.job_queue
    jq.run_daily(
        daily.push_daily_suggested_order, time=datetime.time(15, 17),
        days=tuple(range(5))
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
