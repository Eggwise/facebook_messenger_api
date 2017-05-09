from facebook_messenger_api import MessengerBot
from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot, get_test_recipient


def test_text_message():
    print('Testing text message')
    bot = get_test_bot()
    recipient = get_test_recipient()
    message = Message(text='This is a test')
    response, success = bot.send_message(message, recipient)

    print('Success? {0}'.format(success))
    print('Response: {0}'.format(response))


test_text_message()
