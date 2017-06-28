from pony.orm import Database
import os

class DbConfig:
    database = Database('mysql', host=os.getenv('MYSQL_HOST','localhost')\
                , user=os.getenv('MYSQL_USER','sitechecker')\
                , passwd=os.getenv('MYSQL_PASSWORD','sitechecker')\
                , db=os.getenv('MYSQL_DATABASE','test_sitechecker'))



