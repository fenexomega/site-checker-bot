#!/usr/bin/python3 
# -*- coding: utf-8 -*-
# Simple bot to reply messages

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
from sitechecker import SiteChecker 

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)
siteChecker = None

help_text = """
Hello, you can use the following commands:

/help - Show this help.
/subscrible *URL* - Subscrible to receive notifications when the site in the URL changes.
[NOT IMPLEMENTED YET] /unsubscrible *URL* - Unsubscrible from the URL.
[NOT IMPLEMENTED YET] /list - List your Subscriptions.
"""

# Define a few command handlers. These usually take two argumentos bot and update. Error handlers also receive the raise TelegramError object in error.
def start(bot, update):
    user_id = update.message.chat_id
    siteChecker.registerUser(user_id)
    update.message.reply_text('Hi. Type the /help command to start.')

def help(bot, update):
    update.message.reply_text(help_text)

def subscrible(bot, update,args):
    url = args[0]
    url = url.replace('www.','')
    if not 'http://' in url:
        url = 'http://' + url
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


def unsubscrible(bot, update,args):
    url = args[0]
    url = url.replace('www.','')
    if not 'http://' in url:
        url = 'http://' + url
    chat_id = update.message.chat_id
    if siteChecker.unsubscribleURL(url, chat_id):
        text = 'Your subscription to {} has been deleted.'.format(url)
    else:
        text = 'You\'re not subscribed to this site'    
    update.message.reply_text(text=text)
    return


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"'.format(update,error))

def main():
    #Create the EventHandler and pass it your bot's token.
    bot     = telegram.Bot(os.environ.get('TELEGRAM_BOT_TOKEN'))
    updater = Updater(bot=bot)
    
# Get the dispatcher to register handlers
    dp = updater.dispatcher

    #set the commands
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("subscrible",
        subscrible,pass_args=True))
    dp.add_handler(CommandHandler("unsubscrible",
        unsubscrible,pass_args=True))
    dp.add_handler(CommandHandler("list",list))
    dp.add_handler(CommandHandler("help",help))

#   log all errors
    dp.add_error_handler(error)

#   start
    updater.start_polling()

    global siteChecker
    siteChecker = SiteChecker(bot)
    siteChecker.Run()
    



if __name__ == "__main__":
    main()
