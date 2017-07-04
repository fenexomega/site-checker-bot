site-notifier-telegram-bot
==========================

A bot to notify when a website changes.

This bot compares two screenshots of the website to see if it has changed.
If it has, then the bot will send a notification to the user.

## Commands
* /help - Display this command list.
* /list - List your subscribes.
* /subscribe URL - Subscrible to receive changes from the URL.
* /unsubscrible URL  - Unsubscrible to stop receiving subscribles from this URL.

## Requirements

You need to have _NPM_, _NodeJS_ and _Python3_ installed in your Linux box.

After that, run the script located at `scripts/install`, and then you're set.

## Configuration

This bot uses the file `/etc/sitecheckerbot.conf` for configuration. There you have some enviroment variables to set.
The most important of then is `TELEGRAM_BOT_TOKEN`. On that one you'll set the Telegram Bot Token you get from The Bot Father.
