from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot, get_test_recipient



def test_bot():

    print('Testing text message')
    bot = get_test_bot()
    recipient = get_test_recipient()

    bot.typing_on()

    print('Success? {0}'.format(success))
    print('Response: {0}'.format(response))