#!/usr/bin/python3 
# -*- coding: utf-8 -*-
# Simple bot to reply messages

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
from sitechecker import SiteChecker 

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take two argumentos bot and update. Error handlers also receive the raise TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')

def echo(bot, update):
    print(update.message.chat_id)
    # para ver o usuário -> update.effective_user
    print(update.effective_user)
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"'.format(update,error))

def main():
    #Create the EventHandler and pass it your bot's token.
    bot     = telegram.Bot('TOKEN')
    updater = Updater(bot=bot)
    
# Get the dispatcher to register handlers
    dp = updater.dispatcher

    #set the commands
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",help))

#on noncommand i.e. message- do this
    dp.add_handler(MessageHandler(Filters.text,echo))

#   log all errors
    dp.add_error_handler(error)

#   start
    updater.start_polling()

    obj = SiteChecker(bot)
    obj.Run()
    



if __name__ == "__main__":
    main()
