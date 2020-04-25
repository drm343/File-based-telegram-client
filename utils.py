#!/usr/bin/env python
from typing import Tuple, List

import os
import tempfile
import glob
import datetime


SPLIT_TOKEN = '+'


def replace_47(string : str) -> str:
    return string.replace('/', '0x2F')


def search_file_or_create(id : str, danger_title : str, path : str) -> str:
    result = glob.glob(f'{path}/{id}*')

    title = replace_47(danger_title)
    if result == []:
        file = f'{id}{SPLIT_TOKEN}{title}.'
        return tempfile.mkstemp(prefix = file, dir = f'{path}')[1]
    else:
        return result[0]


def search_dir_or_create(path : str) -> str:
    result = glob.glob(f'./{path}*')

    if result == []:
        os.mkdir(path)
        return path
    else:
        return result[0]


def split(file_name : str) -> Tuple[str, str]:
    name = os.path.splitext(os.path.basename(file_name))[0]
    return name.split(SPLIT_TOKEN)


def search(id : str, path : str) -> List[str]:
    return glob.glob(f'{path}/{id}*')


def build_from_message(update):
    message_root = update['message']

    # message
    message_content = message_root['content'].get('text', {})
    message_text = message_content.get('text', '')

    # id
    chat_id = message_root['chat_id']
    reply_id = message_root['id']

    # user
    user_id = message_root['sender_user_id']

    # date
    date_context = message_root['date']
    date = datetime.datetime.fromtimestamp(date_context)

    return {'text': message_text,
            'user_id': user_id,
            'chat_id': chat_id,
            'reply_id': reply_id,
            'date': date, }


def real_filter(f, l):
    result = []

    for i in l:
        check = f(i)

        if check != False:
            result.append(check)
    return result


def check_user(f, user):
    try:
        result = f(user)
    except:
        result = False
    return result


def get_first_name(user):
    action = [lambda x: x['first_name'],
              lambda x: x['username'],
              lambda x: 'anonymous'
              ]

    return real_filter(lambda f: check_user(f, user), action)[0]
