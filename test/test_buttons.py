from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot_with_recipient
from facebook_messenger_api import PostBackButton, UrlButton, CallButton, ShareButton, GenericTemplateMessage, GenericElement


def test_buttons():
    print('Testing buttons')
    bot = get_test_bot_with_recipient()

    bot.send_text_message('Testing postback button')
    test_button_postback()

    bot.send_text_message('Testing url button')
    test_button_url()

    bot.send_text_message('Testing call button')
    test_button_call()

    bot.send_text_message('Testing share button')
    test_button_share()

    print('Testing done')



def send_buttons(buttons):

    bot = get_test_bot_with_recipient()
    if not isinstance(buttons, list):
        buttons = [buttons]
    print('Sending buttons', buttons)

    subtitle = '\n'.join([str(i.__class__.__name__) for i in buttons])
    element = GenericElement(buttons=buttons, title='Generic Element with buttons', subtitle=subtitle)

    elements = [element]
    message = GenericTemplateMessage(elements=elements)
    response, success = bot.send_message(message)

    print('Response: ', response)
    print('Success? ', success)


def test_button_postback():
    button_postback = PostBackButton(title='Postback button', payload='BUTTON PAYLOAD')
    send_buttons(button_postback)

def test_button_url():
    some_url = 'https://google.com'
    button_url = UrlButton(url=some_url, title='Url button', webview_height_ratio=UrlButton.WEBVIEW_HEIGHT_RATIO.COMPACT)
    send_buttons(button_url)
    pass

def test_button_call():
    button_call_number = 'some_phone_number'
    button_call = CallButton(title='Call button', payload=button_call_number)
    send_buttons(button_call)
    pass

def test_button_share():
    button_share = ShareButton()
    send_buttons(button_share)
    pass


def test_some_buttons():
    some_url = 'https://google.com'
    button_url = UrlButton(url=some_url, title='Url button')

    button_call_number = 'some_phone_number'
    button_call = CallButton(title='Call button', payload=button_call_number)

    button_postback = PostBackButton(title='Postback button', payload='BUTTON PAYLOAD')

    buttons = [button_url, button_call, button_postback]
    send_buttons(buttons)


test_button_url()
# test_button_share()
# test_button_call()
# test_button_postback()

# test_buttons()

# test_some_buttons()