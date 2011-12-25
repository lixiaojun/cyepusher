# -*- coding: utf-8 -*-
'''
Created on 2011-12-8

@author: lixiaojun
'''
from jobs.models import cyetbReflector
from libs.cyetools import logger
from twisted.enterprise import reflector




class Task(object):
    def __init__(self, name):
        self.name = name
        
    def __call__(self):
        say = 'Hello, %s' % self.name
        print say
        logger.info('Task say: %s' % say)
        
class CyeTask(object):
    def __init_(self, id):
        self.id = id;
    
    def __call__(self):
        info = 'Fetch cye data by id = 1'
        print info
        logger.info('Task: '+info)
        d = cyetbReflector.loadObjectsFrom('cye_tb', whereClause=[("id", reflector.EQUAL, self.id)])
        print d
        