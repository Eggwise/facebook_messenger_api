from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot_with_recipient
from facebook_messenger_api import PostBackButton, UrlButton, CallButton, ShareButton, GenericTemplateMessage, GenericElement

from facebook_messenger_api import ListTemplateMessage, ListTemplate, ListElement

def test():


    element_1 = ListElement(title='Title', subtitle='Subtitle')

    page = ListTemplateMessage(elements=[element_1, element_1, element_1])

    bot = get_test_bot_with_recipient()

    bot.send_message(page)
    pass


test()