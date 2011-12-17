# -*- coding: utf-8 -*-
'''
Created on 2011-12-8

@author: lixiaojun
'''
from libs.cyetools import logger

class Task(object):
    def __init__(self, name):
        self.name = name
        
    def __call__(self):
        say = 'Hello, %s' % self.name
        print say
        logger.info('Task say: %s' % say)