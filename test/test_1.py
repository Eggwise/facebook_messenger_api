from facebook_messenger_api import MessengerBot
from facebook_messenger_api import Message
import logging
logging.basicConfig(level=logging.DEBUG)

from facebook_messenger_api.test.utils import get_test_bot, get_test_recipient

bot = get_test_bot()
recipient = get_test_recipient()

message = Message(text='This is a test')

response, success = bot.send_message(message, recipient)

print(response, success)
