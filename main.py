#!/usr/bin/env python
from typing import Tuple
import os
from functools import reduce
import functools
import tempfile
import importlib

import pyinotify

import tg
from tg import get_telegram_client
import utils


class Message(pyinotify.ProcessEvent):
    def my_init(self, client):
        self.command = "command"
        self.client = client

    def process_IN_MODIFY(self, event):
        if event.name == self.command:
            return

        id, title = utils.split(event.name)
        chat_id = int(id)

        with open(event.pathname, "r") as f:
            lines = f.readlines()

            if len(lines) == 1:
                self.client.send_message(
                        chat_id = chat_id,
                        text = lines[0].rstrip(),
                        )
            else:
                command = lines[0].split()
                action = {'reply': self.reply,
                        }
                action[command[0]](chat_id, command, lines)

    def reply(self, chat_id, command, lines):
        pass
#        _, reply_id = command
#        strip_join = lambda x, y: x.join(y.rstrip())
#        message = reduce(strip_join, lines[1:], '')
#
#        self.client.send_message(
#                chat_id = chat_id,
#                reply_id = int(reply_id),
#                text = message,
#                )


class Command(pyinotify.ProcessEvent):
    def my_init(self):
        self.command = "command"

    def process_IN_MODIFY(self, event):
        if event.name == self.command:

            with open(event.pathname, "r") as f:
                lines = f.readlines()

                command = lines[0].split()
                action = {'reload': self.reload,
                        }

                action.get(command[0], lambda x: x)(lines)


    def reload(self, lines):
        importlib.reload(utils)
        #importlib.reload(tg)
        print('reload success')


pipe = utils.search_dir_or_create("pipe")

wm = pyinotify.WatchManager()
handler = Command(Message(client = get_telegram_client(pipe)))
notifier = pyinotify.Notifier(wm, default_proc_fun = handler)
wm.add_watch(pipe, pyinotify.IN_MODIFY)
notifier.loop()
