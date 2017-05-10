import os
from facebook_messenger_api import MessengerBot
import logging

def _validate_credentials(config):
    if config is None:
        msg = 'Corrupt credentials config'
        raise Exception(msg)
    if 'access_token' not in config:
        msg = 'No page access token defined in test credentials config'
        raise Exception(msg)
    if 'recipient_id' not in config:
        msg = 'No recipient id defined in test credentials config'
        raise Exception(msg)


def _load_credentials(file_name, loader):
    path = os.path.join(os.path.dirname(__file__), file_name)
    log_msg = 'Reading credentials from path: {0}'.format(path)
    logging.info(log_msg)

    with open(path) as f:
        credentials = loader.load(f.read())
        _validate_credentials(credentials)
        return credentials


def _get_credentials_yaml():
    import yaml
    CONFIG_FILE_NAME = 'config.yml'
    credentials = _load_credentials(CONFIG_FILE_NAME, yaml)
    return credentials


def _get_credentials_json():
    import json
    CONFIG_FILE_NAME = 'config.json'
    credentials = _load_credentials(CONFIG_FILE_NAME, json)
    return credentials


def _get_credentials():
    try:
        credentials = _get_credentials_yaml()
        return credentials
    except Exception as e:
        print('Failed to read credentials from yaml file')
        print('Error: {0}'.format(e))

    try:
        print('Getting credentials from json file')
        credentials = _get_credentials_json()
        return credentials
    except Exception as e:
        print('Failed to read credentials from json file')
        print('Error: {0}'.format(e))
        raise


def get_test_recipient():
    credentials = _get_credentials()
    recipient_id = str(credentials['recipient_id'])
    return recipient_id


def get_test_bot():
    credentials = _get_credentials()
    bot = MessengerBot(credentials['access_token'])
    return bot

def get_test_bot_with_recipient():
    credentials = _get_credentials()
    page_access_token = credentials['access_token']
    recipient = credentials['recipient_id']
    bot = MessengerBot(page_access_token, recipient)
    return bot