# -*- coding: utf-8 -*-
'''
Created on 2011-10-8

@author: qianmu.lxj
'''
from jobs.CyeFilterInc import JingdongFilter
from jobs.models import cyeTbReflector, CyeTbRow
from libs.cyetools import cyeDBpoool
from twisted.enterprise import reflector
import random
import time

#from mypython.a import add_func
def onInsert(data):
    print 'completed'
    print data

def gotCye(datas):
    for data in datas:
        print "Got:", data.id
        
def getCyeData():
    return cyeDBpoool.runQuery("SELECT * FROM cye_tb")

def printResult(l):
    if l:
        print l
    else:
        print "No such data"
    
if __name__ == '__main__':
    
    fp = open('detail.dat')
    html = fp.read()
    fp.close()
    
    detail = JingdongFilter.handleDetail(html)
    
    #print detail
    
    newItem = CyeTbRow()
    newItem.key = 'test'+str(random.randint(1, 999))
    newItem.title = 'test'
    newItem.url = 'url'
    newItem.product_img_url = 'product_img_url'
    newItem.product_img = 'product_img'
    newItem.detail = 'detail'
    newItem.utime = time.strftime('%Y-%m-%d %X', time.localtime())
    
    #cyeTbReflector.insertRow(newItem).addCallback(onInsert)
    
    d = cyeTbReflector.loadObjectsFrom("cye_tb")
    
    d.addCallback(gotCye)
    print 'hello'
    
    getCyeData().addCallback(printResult)
    
    pass