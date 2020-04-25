# File-based telegram client

This is a concept project for tglib.
You can use any editor what you like to communicate with telegram.
Or command cat to do that.

Client will create 2 files in log and pipe directory.
Files in log is messages from telegram.
Files in pipe will send message to telegram. 

# Require

 - bash >= 5.0.17
 - Python >= 3.8.2
 - fzf **(optional)** >= 0.21.0
 - vim **(optional)** >= 8.2

# Prepare

## Step 1

Run make to prepare python3 environment.

## Step 2 (optional for vim)

Install fzf.
https://github.com/junegunn/fzf#installation

# How to use

## Step 1

"**source venv/bin/activate**" to enter python3 environment.

## Step 2

Edit tg.json with your login information.
Get app id and app hash from **https://my.telegram.org/apps**.

Run "**./rc.tg start**" to start client.
Use "**./rc.tg stop**" to stop client.

## Step 3 : login for first time.

If you see a file named "**login_code**" in current directory.
You need to type your "login code" to this file and save it.
If this file disappear, then you are login success.

## Step 4 : Chat with file.

Telegram will send message to you.
It will save in log and create a file in pipe.
Read file in log to see chat message.
Write 1 line message to file in pipe will send message to telegram.

Vim user can run "**./rc.tg editor**", then select a chat.
Chat history will show in top window.
Write 1 line message in bottom window and save, it will send message to telegram.

# Known issue

 - Can't reply message.
 - Will lost some message if program error.
 - Will lost some message if other client mark messages as read.
 - Not implement reload chat history (will fix previous 2 issue).
