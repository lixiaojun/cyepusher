# -*- coding: utf-8 -*-
'''
Created on 2011-12-4

@author: lixiaojun
'''

import logging


logger = logging.getLogger()
hdlr = logging.FileHandler('logs/threadpool.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

logger.setLevel(logging.NOTSET)