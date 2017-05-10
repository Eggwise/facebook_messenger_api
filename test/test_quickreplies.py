from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot_with_recipient
from facebook_messenger_api import QuickReply, QuickReplyMessage


def test_quick_reply():
    print('Testing quick reply')
    bot = get_test_bot_with_recipient()

    quickreply_location = QuickReply(content_type=QuickReply.CONTENT_TYPE.LOCATION)
    quickreply_text = QuickReply(title='Text quickreply', content_type=QuickReply.CONTENT_TYPE.TEXT, payload='MUST HAVE PAYLOAD')
    quickreply_image = QuickReply(image_url='https://placehold.it/100x100', title='With image', content_type=QuickReply.CONTENT_TYPE.TEXT, payload='MUST HAVE PAYLOAD')

    quickreplies = [quickreply_location, quickreply_text, quickreply_image]

    quickreply_message = QuickReplyMessage(text='Quicklrepies test', quick_replies=quickreplies)
    response, success = bot.send_message(quickreply_message)

    print('Response: ', response)
    print('Success? ', success)



def test_invalid_quick_reply():
    bot = get_test_bot_with_recipient()

    #no payload
    quickreply_text = QuickReply(title='Text quickreply')

test_invalid_quick_reply()

# test_quick_reply()

