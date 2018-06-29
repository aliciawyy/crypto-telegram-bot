from crypto_telegram_bot import utils


def test_command_enum_command():
    assert utils.CommandEnum.CHOOSE_EXCHANGE.lower() == "choose_exchange"
    assert utils.CommandEnum.CHOOSE_EXCHANGE.command() == "/choose_exchange"
