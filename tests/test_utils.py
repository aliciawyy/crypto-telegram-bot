from crypto_telegram_bot import utils


def test_command_enum_command():
    assert utils.CommandEnum.CHOOSE_EXCHANGE.lower() == "choose_exchange"
    assert utils.CommandEnum.CHOOSE_EXCHANGE.command() == "/choose_exchange"


def test_user_info_enum():
    assert utils.UserInfoEnum.API_KEY.name == "API_KEY"
    assert utils.UserInfoEnum.API_KEY.lower() == "api_key"
