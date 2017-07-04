#!/usr/bin/python3 
# -*- coding: utf-8 -*-
# Simple bot to reply messages

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import configparser
from sitecheckerbot.sitechecker import SiteChecker 

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

help_text = """
Hello, you can use the following commands:

/help - Show this help.
/subscribe _URL_ - Subscrible to receive notifications when the site in the URL changes.
/unsubscribe _URL_ - Unsubscribe from the URL.
/list - List your Subscriptions.
"""

def parseUrl(url):
    url = url.replace('www.','')
    if not 'http://' in url:
        url = 'http://' + url
    return url

dp = None
# Define a few command handlers. These usually take two argumentos bot and update. Error handlers also receive the raise TelegramError object in error.
def start(bot, update):
    user_id = update.message.chat_id
    siteChecker.registerUser(user_id)
    update.message.reply_text('Hi. Type the /help command to start.')

def help(bot, update):
    update.message.reply_text(help_text)

def subscribe(bot, update,args):
    if len(args) != 1:
        update.message.reply_text('This option requires exactly one argument')
        return
    url = parseUrl(args[0])
    siteChecker.registerURL(url,update.message.chat_id)
    update.message.reply_text("You're now subscribed to {}.".format(url))

def list(bot, update):
    chat_id = update.message.chat_id
    l = siteChecker.getUrlsFromUser(chat_id)
    s = 'Your pages are:\n'
    for x in l:
        s += '* ' +  x + '\n'
    update.message.reply_text(text=s)
    return


def unsubscribe(bot, update,args):
    if len(args) != 1:
        update.message.reply_text('This option requires exactly one argument')
        return
    url = parseUrl(args[0])
    chat_id = update.message.chat_id
    if siteChecker.unsubscribeURL(url, chat_id):
        text = 'Your subscription to {} has been deleted.'.format(url)
    else:
        text = 'You\'re not subscribed to this site'    
    update.message.reply_text(text=text)
    return


def error(bot, update, error):
    logger.warn('Update "{}" caused error "{}"'.format(update,error))

def main():
    #Create the EventHandler and pass it your bot's token.
    # bot     = telegram.Bot(os.environ.get('TELEGRAM_BOT_TOKEN'))
    # updater = Updater(bot=bot)
    updater = Updater(os.environ.get('TELEGRAM_BOT_TOKEN'))
    bot = updater.bot
    
# Get the dispatcher to register handlers
    global dp
    dp = updater.dispatcher

    #set the commands
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("subscribe",
        subscribe,pass_args=True))
    dp.add_handler(CommandHandler("unsubscribe",
        unsubscribe,pass_args=True))
    dp.add_handler(CommandHandler("list",list))
    dp.add_handler(CommandHandler("help",help))

#   log all errors
    dp.add_error_handler(error)

#   start
    updater.start_polling()

    global siteChecker
    siteChecker = SiteChecker(bot)
    try:
        siteChecker.Run()
    except (KeyboardInterrupt, SystemExit):
        logger.warn('Stopping bot')
        updater.stop()


if __name__ == "__main__":
    main()
