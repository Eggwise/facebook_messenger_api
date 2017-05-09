import requests, json


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

        print('send message', data)
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            print('ERROR')
            print(r.status_code)
            print(r.text)

    def send_message(self, message, recipient=None):
        if recipient is not None:
            message.recipient = recipient

        message = message.build()
        self._send_message(self.access_token, message)
