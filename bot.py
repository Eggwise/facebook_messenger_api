import requests, json
import logging
from .models.models import *


class Bot():
    def __init__(self, access_token, recipient=None):
        self.access_token = access_token
        self._recipient = recipient

    @property
    def recipient(self):
        if self._recipient is None:
            raise AttributeError('No recipient provided')
        return self._recipient

    @classmethod
    def _send_message(cls, access_token, message):
        params = {
            "access_token": access_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps(message)

        logging.info('Sending message: {0}'.format(data))
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            success = False
            logging.error('Send message response returned non 200 status code')
            logging.error('Response: {0}'.format(r.text))

        else:
            success = True
        response = r.text
        return response, success

    def send_message(self, message, recipient=None):

        if recipient is None:
            recipient = self.recipient

        message.recipient = recipient

        message = message.build()
        response = self._send_message(self.access_token, message)
        return response

    def send_text_message(self, text, recipient=None):
        if recipient is None:
            recipient = self.recipient
        message = Message(text=text)
        return self.send_message(message, recipient)

    def _set_typing(self, on=True, recipient=None):
        if recipient is None:
            recipient = self.recipient
        if on:
            action = Message.ACTION.TYPING_ON
        else:
            action = Message.ACTION.TYPING_OFF

        message = Message(action=action)
        response, success = self.send_message(message, recipient)
        return response, success

    def typing_on(self, recipient=None):
        return self._set_typing(True, recipient)

    def typing_off(self, recipient=None):
        return self._set_typing(recipient, recipient)

    def mark_seen(self, recipient=None):
        if recipient is None:
            recipient = self.recipient

        action = Message.ACTION.MARK_SEEN
        message = Message(action=action)
        return self.send_message(message, recipient)
