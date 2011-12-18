# -*- coding: utf-8 -*-
'''
Created on 2011-12-8

@author: lixiaojun
'''
from libs.cyetools import logger, giftDBpoool
from twisted.enterprise import row
from twisted.enterprise.sqlreflector import SQLReflector

class ProductRow(row.RowObject):
    rowColumns = [("id", "int"),
                  ("key", "varchar"),
                  ("title", "varchar"),
                  ("url", "varchar"),
                  ("name", "varchar"),
                  ("add_time", "varchar"),
                  ("image", "varchar"),
                  ("origin_image_url", "varchar"),
                  ("producer", "varchar"),
                  ("production_place", "varchar"),
                  ("gross_weight", "varchar"),
                  ("status", "varchar")]
    rowKeyColumns = [("key", "varchar")]
    rowTableName = "product"
    
productReflector = SQLReflector(giftDBpoool, [ProductRow])


class Task(object):
    def __init__(self, name):
        self.name = name
        
    def __call__(self):
        say = 'Hello, %s' % self.name
        print say
        logger.info('Task say: %s' % say)