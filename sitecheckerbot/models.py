# -*- coding: utf-8 -*-
from pony.orm import *
from settings import DbConfig

db = DbConfig.database

class Site(db.Entity):
    url = Required(str,unique=True)
    last_modification = Required(str)
    users = Set('User')

class User(db.Entity):
    sites = Set(Site,reverse='users')
    chat_id = Required(int,unique=True)
    email   = Optional(str)

db.generate_mapping(create_tables=True)
