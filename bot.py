import requests, json
import logging


class Bot():
    def __init__(self, access_token):
        self.access_token = access_token

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
        if recipient is not None:
            message.recipient = recipient

        message = message.build()
        response = self._send_message(self.access_token, message)
        return response
