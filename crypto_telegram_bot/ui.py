import logging

from . import tl
from . import utils
from . import register

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    utils.print_bot_information()

    updater = utils.updater(token=utils.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(register.workflow_handler())
    dp.add_handler(tl.MessageHandler(tl.Filters.command, register.unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
