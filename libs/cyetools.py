# -*- coding: utf-8 -*-
'''
Created on 2011-12-4

@author: lixiaojun
'''

from twisted.enterprise import adbapi
import ConfigParser
import logging
import os
import time

'''
read cfg file
'''
cf = ConfigParser.ConfigParser()
cf.read('pusher.cfg')

logger = logging.getLogger()
#tplog = cf.get('log', 'threadpool')
hdlr = logging.FileHandler('logs/threadpool.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

logger.setLevel(logging.NOTSET)


'''
Connect database
'''
DB_HOST = cf.get('db', 'db_host')
DB_PORT = cf.get('db', 'db_port')
DB_USER = cf.get('db', 'db_user')
DB_PASSWORD = cf.get('db', 'db_password')

cyeDBpoool = adbapi.ConnectionPool('MySQLdb', host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database='cye_db')
giftDBpoool = adbapi.ConnectionPool("MySQLdb", host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database='mygift')

