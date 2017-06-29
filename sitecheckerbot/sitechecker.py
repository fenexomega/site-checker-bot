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
        s = None
        try:
            d = self.getSiteLastModification(URL)
            # http://strftime.org/
            # date = datetime.datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %Z')
            s = Site(url=URL,last_modification=d)  
            commit()
        except TransactionIntegrityError:
            pass

        s = Site.get(url=URL)
        u = User.get(chat_id=chat_id)
        if u == None:
            u = User(chat_id=chat_id)
        u.sites.add(s)
        commit()
        
    @db_session
    def unsubscribleURL(self, URL,chat_id):
        s = None
        try: 
            s = Site.get(url=URL)
        except TransactionIntegrityError:
            return False
        u = User.get(chat_id=chat_id)
        if not s in u.sites:
            return False
        u.sites.remove(s)
        commit()
        return True


    def siteHasChanged(self,site):
        d = self.getSiteLastModification(site.url)
        return site.last_modification != d

    def getSiteLastModification(self, url):
        try:
            r = requests.get(url)
            return r.headers['Last-Modified']
        except OSError:
            return 'offline'
        except ConnectionError:
            return 'offline'

    @db_session 
    def updateSiteRecord(self, site):
        site.last_modification = self.getSiteLastModification(site.url)
        commit()


    def notify(self,site):
        message = "Hello, the site {} has changed. The last modification \
                was at {}.".format(site.url,site.last_modification)
        message_offline = "Hello. The site {} is now offline.".format(site.url)
        for user in site.users:
            text = message
            if site.last_modification == 'offline':
                text=message_offline
            self.bot.send_message(chat_id=user.chat_id,text=text)

    @db_session
    def getUrlsFromUser(self,chat_id):
        u = User.get(chat_id=chat_id)
        return [ s.url for s in u.sites]

    @db_session
    def registerUser(self,user_id):
        u = User(chat_id=user_id)
        commit()

    @db_session
    def checkUrls(self):
        for s in Site.select():
            if self.siteHasChanged(s):
                self.updateSiteRecord(s)
                self.notify(s)
    
    def Run(self):
        while True:
            self.checkUrls()
            sleep(5)
            
