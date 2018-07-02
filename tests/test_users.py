from os import path
from unittest import TestCase, mock

from crypto_telegram_bot import users


class UsersTest(TestCase):
    def setUp(self):
        filename = path.join(path.dirname(__file__), "data", "users.json")
        self.users = users.Users(filename)
        self.user_id = "452516"

    @mock.patch("json.dump")
    def test_add(self, m_dump):
        info = {"index": "CRC3"}
        with mock.patch("builtins.open"):
            self.users.add(self.user_id, info)
        args, kwargs = m_dump.call_args
        assert args[0] == self.users.data
        assert info == self.users[self.user_id]

    def test_contains(self):
        assert self.user_id not in self.users
        assert "32516" in self.users
