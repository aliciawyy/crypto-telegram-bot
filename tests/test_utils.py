from crypto_telegram_bot import utils


def test_command_enum_text():
    assert utils.CommandEnum.REGISTER.text() == "register"


def test_command_enum_command():
    assert utils.CommandEnum.REGISTER.command() == "/register"
