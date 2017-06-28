# -*- coding: utf-8 -*-

import requests
from time import sleep
from pony import *


from dbconfig import DbConfig
from models import *

class SiteChecker:
    
    def __init__(self, bot):
        self.bot = bot
        db = DbConfig.database

    @db_session
    def registerURL(self, URL,chat_id):
        try:
            r = requests.get(URL)
            d = r.headers['Last-Modified']
            # http://strftime.org/
            # date = datetime.datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %Z')
            s = Site(url=URL,last_modification=d)  
            commit()
        except OSError:
            print("URL not found")
        except TransactionIntegrityError:
            print("URL already exists")

        # try:
            s = Site.get(url=URL)
            u = User.get(chat_id=chat_id)
            if u == None:
                u = User(chat_id=chat_id)
            u.sites.add(s)
            commit()
        # except Exception:
            print('whut')
        

    def Run(self):
        while True:
           self.bot.send_message(chat_id=71321790,text='Hello Jordy')
           sleep(5)



def main():
    sc = SiteChecker(None)
    sc.registerURL('http://pudim.com.br',123)

if __name__ == "__main__":
    main()
