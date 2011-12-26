'''
Created on 2011-12-24

@author: qianmu.lxj
'''
from libs.cyetools import giftDBpoool, cyeDBpoool
from twisted.enterprise import row
from twisted.enterprise.sqlreflector import SQLReflector

class ProductRow(row.RowObject):
    rowColumns = [("id", "int"),
                  ("key", "varchar"),
                  ("title", "varchar"),
                  ("url", "varchar"),
                  ("name", "varchar"),
                  ("add_time", "datetime"),
                  ("image", "varchar"),
                  ("origin_image_url", "varchar"),
                  ("producer", "varchar"),
                  ("production_place", "varchar"),
                  ("gross_weight", "varchar"),
                  ("status", "varchar"),
                  ("utime", "datetime")]
    rowKeyColumns = [("key", "varchar")]
    rowTableName = "product"
    
class CyeTbRow(row.RowObject):
    rowColumns = [("id", "int"),
                  ("key", "varchar"),
                  ("url", "varchar"),
                  ("title", "varchar"),
                  ("product_img_url", "varchar"),
                  ("product_img", "varchar"),
                  ("detail", "varchar"),
                  ("utime", "time")]
    rowKeyColumns = [("id", "int4")]
    rowTableName = "cye_tb"
    
class CyePriceTbRow(row.RowObject):
    rowColumns = [("id", "int"),
                  ("cye_key", "varchar"),
                  ("price", "varchar"),
                  ("price_img_url", "varchar"),
                  ("product_img_url", "varchar"),
                  ("ctime", "time")]
    rowKeyColumns = [("id", "int4")]
    rowTableName = "cye_price_tb"

class CyeJobTbRow(row.RowObject):
    rowColumns = [("id", "int"),
                  ("job", "text"),
                  ("status", "varchar"),
                  ("ctime", "time")]
    rowKeyColumns = [("id", "int4")]
    rowTableName = "cye_job_tb"
    

    
productReflector = SQLReflector(giftDBpoool, [ProductRow])

cyeTbReflector = SQLReflector(cyeDBpoool, [CyeTbRow])

cyePriceTbReflector = SQLReflector(cyeDBpoool, [CyePriceTbRow])

cyeJobReflector = SQLReflector(cyeDBpoool, [CyeJobTbRow])
