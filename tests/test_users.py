from os import path
import mock
from unittest import TestCase

from crypto_telegram_bot.users import Users


class UsersTest(TestCase):
    def setUp(self):
        filename = path.join(path.dirname(__file__), "data", "users.json")
        self.users = Users(filename)

    @mock.patch("json.dump")
    def test_add(self, m_dump):
        user_id = "452516"
        info = {"index": "CRC3"}
        self.users.add(user_id, info)
        args, kwargs = m_dump.call_args
        assert args[0] == self.users.data
        assert info == self.users[user_id]
