from facebook_messenger_api import Message
import logging

logging.basicConfig(level=logging.INFO)

from facebook_messenger_api.test.utils import get_test_bot_with_recipient
from facebook_messenger_api import PostBackButton, UrlButton, CallButton, ShareButton, GenericTemplateMessage, GenericElement

from facebook_messenger_api import ListTemplateMessage, ListElement

def test():

    element_1 = ListElement(title='Title', subtitle='Subtitle')
    page = ListTemplateMessage(elements=[element_1, element_1, element_1])

    bot = get_test_bot_with_recipient()

    bot.send_message(page)
    pass

def test_large():

    element_1 = ListElement(title='Header', subtitle='Header subtitle', image_url='https://placehold.it/350x350')
    element_2 = ListElement(title='Title', subtitle='Subtitle')
    page = ListTemplateMessage(top_element_style=ListTemplateMessage.TOP_ELEMENT_STYLE.LARGE, elements=[element_1, element_2, element_2])

    bot = get_test_bot_with_recipient()

    bot.send_message(page)
    pass

def test_with_global_button():

    button = PostBackButton(payload='Some payload', title='CLick me')
    element_1 = ListElement(title='Title', subtitle='Subtitle', buttons=[button])
    page = ListTemplateMessage(elements=[element_1, element_1, element_1], buttons=[button])

    bot = get_test_bot_with_recipient()
    bot.send_message(page)

def test_with_buttons():

    button = PostBackButton(payload='Some payload', title='CLick me')
    element_1 = ListElement(title='Title', subtitle='Subtitle', buttons=[button])
    page = ListTemplateMessage(elements=[element_1, element_1, element_1], buttons=[button])

    bot = get_test_bot_with_recipient()
    bot.send_message(page)

def test_with_images():
    some_image = 'placehold.it/350x350'
    button = PostBackButton(payload='Some payload', title='CLick me')
    element_1 = ListElement(title='Image element', subtitle='Subtitle here', buttons=[button], image_url=some_image)
    page = ListTemplateMessage(elements=[element_1, element_1, element_1], buttons=[button])

    bot = get_test_bot_with_recipient()
    bot.send_message(page)

def test_with_images_large():
    top_element_style = ListTemplateMessage.TOP_ELEMENT_STYLE.LARGE

    some_image = 'https://placehold.it/350x350'
    header_image = 'https://placehold.it/800x800'

    some_button = PostBackButton(payload='Some payload', title='CLick me')
    element_1 = ListElement(title='Header element', subtitle='Header subtitle', image_url=header_image, buttons=[some_button])
    element_2 = ListElement(title='Image element', subtitle='Subtitle here', buttons=[some_button], image_url=some_image)
    page = ListTemplateMessage(elements=[element_1, element_2, element_2], top_element_style=top_element_style)

    bot = get_test_bot_with_recipient()
    bot.send_message(page)


def test_full():
    top_element_style = ListTemplateMessage.TOP_ELEMENT_STYLE.LARGE


    header_image = 'https://placehold.it/800x800'
    header_button =  PostBackButton(payload='Some payload', title='Cool button me')
    header_element = ListElement(title='Header element', subtitle='Header subtitle', image_url=header_image,
                            buttons=[header_button])

    list_elements = [header_element]

    #button for the list elements
    some_button = PostBackButton(payload='Some payload', title='some button')
    some_image = 'https://placehold.it/350x350'

    for i in range(0, 3):

        element = ListElement(title='List element', subtitle='Subtitle.....e..e..e', image_url=some_image,
                            buttons=[some_button])
        list_elements.append(element)

    global_button = UrlButton('Global button', )

    page = ListTemplateMessage(elements=list_elements, top_element_style=top_element_style, buttons=[global_button])
    bot = get_test_bot_with_recipient()
    bot.send_message(page)


# test()
# test_large()
# test_with_global_button()
# test_with_buttons()
# test_with_images()
# test_with_images_large()
test_full()