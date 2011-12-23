# -*- coding: utf-8 -*-
'''
Created on 2011-11-28

@author: lixiaojun
'''
from jobs.task import CyeTask
from libs import jsonrpc
from libs.cyetools import logger
from libs.threadpool import ThreadPool, TaskQueue, ThreadPoolManager, \
    LoadBalancingThread


def echo(self):
    return 'Hello world!'

def join(sid):
    if sid is None:
        sid = 'cye'
        
    queue = TaskQueue.getInstance()
    queue.addTask(CyeTask(sid))
    return "rpc say: success! "


if __name__ == '__main__':
    
    thread_pool = ThreadPool.getInstance()
    task_queue = TaskQueue.getInstance()
    thread_pool.initPool(10, 25)
    task_queue.initQueue()
    
    pm = ThreadPoolManager(thread_pool, task_queue)
    pm.proceed()
        
    lb = LoadBalancingThread(15, thread_pool)
    lb.proceed()
    
    server = jsonrpc.Server(jsonrpc.JsonRpc20(), jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415), timeout=30.0, logfunc=jsonrpc.log_file("logs/cyepusher_rpc.log")))
    server.register_function(echo)
    server.register_function(join)
    
    server.serve()
