#!/usr/bin/env python
import os
import time
import logging
import datetime
import tempfile
from functools import partial
from pathlib import Path
import json

from telegram.client import Telegram
from telegram.utils import AsyncResult
import utils


logger = logging.getLogger(__name__)


class File_Based (Telegram):
    def _send_telegram_code(self) -> AsyncResult:
        logger.info('Sending code')

        check_file = Path('login_code')
        check_file.touch(mode=0o644)


        while os.stat(check_file).st_size == 0:
            time.sleep(0.1)

        with open(check_file.name, 'r') as f:
            line = f.read()
            code = line.rstrip()
        data = {'@type': 'checkAuthenticationCode', 'code': str(code)}

        check_file.unlink()
        return self._send_data(data, result_id='updateAuthorizationState')


def new_message_handler(update, tg, pipe):
    message = utils.build_from_message(update)
    chat_id = message['chat_id']
    reply_id = message['reply_id']
    user_id = message['user_id']
    date = message['date']
    text = message['text']

    chat = tg.get_chat(chat_id = chat_id)
    chat.wait()
    title = chat.update['title']

    user = tg.get_user(user_id = user_id)
    user.wait()

    # first_name =  user['first_name'] \/
    #               user['username'] \/
    #               'anonymous'.
    if type(user) == AsyncResult:
        first_name = utils.get_first_name(user.update)
    else:
        first_name = utils.get_first_name(user)

    log = utils.search_file_or_create(chat_id, title, "./log")

    utils.search_file_or_create(chat_id, title, pipe)

    print(update)
    print(user)
    with open(log, "a") as f:
        f.write(f'{date} {reply_id}|{first_name}: {text}\n')


def get_telegram_client(pipe):
    with open('tg.json', 'r') as f:
        cfg = json.load(f)

    tg = File_Based(
            api_id = cfg['api_id'],
            api_hash = cfg['api_hash'],
            phone = cfg['phone'],  # you can pass 'bot_token' instead
            database_encryption_key = cfg['database_encryption_key'],
            )
    tg.login()

    handler = partial(new_message_handler, tg = tg, pipe = pipe)
    tg.add_message_handler(handler)
    return tg
