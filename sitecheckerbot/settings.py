import os,sys
import logging
from os.path import join,dirname
from dotenv import load_dotenv
from pony.orm import Database

# Find the variables from .env
load_dotenv(join(dirname(__file__),'.env'))

#use this on the MYSQL database
#create database test_sitechecker character set utf8
class DbConfig:
    try:
        database = Database('mysql', host=os.getenv('MYSQL_HOST','localhost')\
                    , user=os.getenv('MYSQL_USER','sitechecker')\
                    , passwd=os.getenv('MYSQL_PASSWORD','sitechecker')\
                    , db=os.getenv('MYSQL_DATABASE','sitechecker'))
    except Exception as e:
       logger = logging.getLogger(__name__)
       logger.critical('Couldn\'t connect to database due to error "%s"' % e)
       logger.warn('Check if you have a MYSQL connection or have set the env variables correcly')
       sys.exit(2)
       



