from . import tl
from . import utils


def trade_menu(bot, update):
    reply_msg = "Buy or sell?"

    buttons = [
        tl.KeyboardButton(utils.CommandEnum.START.text()),
        tl.KeyboardButton(utils.CommandEnum.CANCEL.text()),
    ]
    cancel_btn = [
        tl.KeyboardButton(utils.CommandEnum.CANCEL.text())
    ]

    menu = utils.build_menu(buttons, n_cols=2, footer_buttons=cancel_btn)
    reply_mrk = tl.ReplyKeyboardMarkup(menu, resize_keyboard=True)
    update.message.reply_text(reply_msg, reply_markup=reply_mrk)


"""
trade_handler = tl.ConversationHandler(
    entry_points=[tl.CommandHandler('register', register)],
    states={
        utils.WorkflowEnum.REGISTER:
            [RegexHandler(comp("^(BUY|SELL)$"), trade_buy_sell, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_CURRENCY:
            [RegexHandler(comp("^(" + regex_coin_or() + ")$"), trade_currency, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True),
             RegexHandler(comp("^(ALL)$"), trade_sell_all)],
        WorkflowEnum.TRADE_SELL_ALL_CONFIRM:
            [RegexHandler(comp("^(YES|NO)$"), trade_sell_all_confirm)],
        WorkflowEnum.TRADE_PRICE:
            [RegexHandler(comp("^((?=.*?\d)\d*[.,]?\d*|MARKET PRICE)$"), trade_price, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOL_TYPE:
            [RegexHandler(comp("^(" + regex_asset_or() + ")$"), trade_vol_asset, pass_chat_data=True),
             RegexHandler(comp("^(VOLUME)$"), trade_vol_volume, pass_chat_data=True),
             RegexHandler(comp("^(ALL)$"), trade_vol_all, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOLUME:
            [RegexHandler(comp("^^(?=.*?\d)\d*[.,]?\d*$"), trade_volume, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_VOLUME_ASSET:
            [RegexHandler(comp("^^(?=.*?\d)\d*[.,]?\d*$"), trade_volume_asset, pass_chat_data=True),
             RegexHandler(comp("^(CANCEL)$"), cancel, pass_chat_data=True)],
        WorkflowEnum.TRADE_CONFIRM:
            [RegexHandler(comp("^(YES|NO)$"), trade_confirm, pass_chat_data=True)]
    },
    fallbacks=[tl.CommandHandler('cancel', cancel, pass_chat_data=True)],
    allow_reentry=True)
"""