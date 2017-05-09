from facebook_messenger_api import MessengerBot
from facebook_messenger_api import Message

from .utils import get_test_bot, get_test_recipient


bot = get_test_bot()
recipient = get_test_recipient()



response, success = bot.send_message('This is a test', recipient)

print(response, success)
