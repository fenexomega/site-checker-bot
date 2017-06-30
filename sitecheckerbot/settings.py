import os
from os.path import join,dirname
from dotenv import load_dotenv
from pony.orm import Database

# Find the variables from .env
load_dotenv(join(dirname(__file__),'.env'))

#use this on the MYSQL database
#create database test_sitechecker character set utf8
class DbConfig:
    database = Database('mysql', host=os.getenv('MYSQL_HOST','localhost')\
                , user=os.getenv('MYSQL_USER','sitechecker')\
                , passwd=os.getenv('MYSQL_PASSWORD','sitechecker')\
                , db=os.getenv('MYSQL_DATABASE','test_sitechecker'))



