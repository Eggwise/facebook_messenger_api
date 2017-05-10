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


def test_typing(on=True):
    print('Testing text message')
    bot = get_test_bot()
    recipient = get_test_recipient()

    #epic action enums
    if on:
        action = Message.ACTION.TYPING_ON
    else:
        action = Message.ACTION.TYPING_OFF

    print(action)
    message = Message(action=action)
    response, success = bot.send_message(message, recipient)

    print('Success? {0}'.format(success))
    print('Response: {0}'.format(response))


def test_natural_message():
    import time

    test_typing()
    time.sleep(2)
    test_text_message()


test_natural_message()
