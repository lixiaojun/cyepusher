# -*- coding: utf-8 -*-
'''
Created on 2011-11-28

@author: lixiaojun
'''

import libs.jsonrpc as jsonrpc
import time
import random
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415), timeout=20.0))

# call a remote-procedure (with positional parameters)

clients = ['chaiyuan', 'qianjie', 'lixioajun', 'chenli', 'huige', 'guqi']
    
for i in range(100000):
    name = clients[random.randint(0, 5)]
    result = server.join(name)
    time.sleep(0.5)
    print result