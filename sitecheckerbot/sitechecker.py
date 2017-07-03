# -*- coding: utf-8 -*-

import requests,socket,os,logging
from time import sleep
from pony import *
from PIL import Image


from sitecheckerbot.settings import DbConfig
from sitecheckerbot.models import *
from sitecheckerbot.helper import Helper


TMP_FILE = '/tmp/screen_bot.png'
SEND_FILE = '/tmp/screen_bot.jpg'
CROP = (0,0,1024,768)

logger = logging.getLogger(__name__)

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
    def unsubscribeURL(self, URL,chat_id):
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
            Helper.takeScreenshot(url,TMP_FILE)
            return Helper.sha1FromFile(TMP_FILE)
        except OSError:
            return 'offline'
        except ConnectionError:
            return 'offline'

    @db_session 
    def updateSiteRecord(self, site):
        site.last_modification = self.getSiteLastModification(site.url)
        commit()


    def notify(self,site):
        message = "Hello, the site {} has changed.".format(site.url)
        message_offline = "Hello. The site {} is now offline.".format(site.url)
        logger.info('enviando notificação {}'.format(site.url))
        self.convertImage(TMP_FILE,SEND_FILE)
        for user in site.users:
            if site.last_modification == 'offline':
                self.bot.send_message(chat_id=user.chat_id,text=message_offline)
            else:
                try:
                    self.bot.send_message(chat_id=user.chat_id,text=message)
                    self.bot.send_photo(chat_id=user.chat_id,photo=open(SEND_FILE,'rb'))
                except Exception as e:
                    print(e)
    
    def convertImage(self,old,new):
        dir =  os.path.dirname(old)
        #save file
        try:
            img = Image.open(old)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.crop(CROP)
            img.save(new)
        except IOError as e:
            print("cannot convert {}".format(e))
        

    @db_session
    def getUrlsFromUser(self,chat_id):
        u = User.get(chat_id=chat_id)
        return [ s.url for s in u.sites]

    @db_session
    def registerUser(self,user_id):
        u = User(chat_id=user_id)
        commit()
        
    def hasInternetConnection(self):
        try: 
            tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp.connect(("8.8.8.8",53)) #google dns
            return True
        except Exception :
            print('No intenret Connection')
            return False

    @db_session
    def checkUrls(self):
        for s in Site.select():
            if not self.hasInternetConnection():
                break
            if self.siteHasChanged(s):
                self.updateSiteRecord(s)
                self.notify(s)
    
    def Run(self):
        while True:
            try:
                if self.hasInternetConnection():
                    self.checkUrls()
                sleep(5)
            except Exception:
                print("Quebrou")
                sys.exit(1)
            
