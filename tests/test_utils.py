from crypto_telegram_bot import utils


def test_command_enum_text():
    assert utils.CommandEnum.REGISTER.text() == "register"
    assert utils.CommandEnum.START.text() == "start"


def test_command_enum_command():
    assert utils.CommandEnum.REGISTER.command() == "/register"
