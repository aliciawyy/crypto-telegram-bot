from os import environ
import logging
from pyrogram import Client
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_ID = environ.get("TEST_TL_API_ID")
API_HASH = environ.get("TEST_TL_API_HASH")

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

app.start()
print(app.get_me())

user = "a_crypto_trading_bot"
res = app.send_message(user, "/start")
m = app.get_messages(
    res["chat"]["id"], [res["message_id"] + 1]
)
print("replies=========\n", m[-1])
app.stop()
