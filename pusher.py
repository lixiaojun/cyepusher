# -*- coding: utf-8 -*-
'''
Created on 2011-12-7

@author: lixiaojun
'''
from jobs.task import Task
from libs import jsonrpc
from libs.daemon import Daemon
from libs.threadpool import ThreadPool, TaskQueue, ThreadPoolManager, \
    LoadBalancingThread
import sys


class CyeDaemon(Daemon):
    def __init__(self, pidfile='pusher.pid', stdin='/dev/null', \
                 stdout='logs/daemon.stdout.log', stderr='logs/daemon.stderr.log'):
        Daemon.__init__(self,pidfile, stdin, stdout, stderr)
        pass
    
    def run(self):
        rpc_server()
        pass
    pass

def rpc_server():
    thread_pool = ThreadPool.getInstance()
    task_queue = TaskQueue.getInstance()
    thread_pool.initPool(10, 25)
    task_queue.initQueue()
    
    pm = ThreadPoolManager(thread_pool, task_queue)
    pm.proceed()
        
    lb = LoadBalancingThread(15, thread_pool)
    lb.proceed()
    
    server = jsonrpc.Server(jsonrpc.JsonRpc20(), \
        jsonrpc.TransportTcpIp(addr=("127.0.0.1", 31415), timeout=30.0, \
                               logfunc=jsonrpc.log_file("logs/cyepusher_rpc.log")))
    #register function
    server.register_function(echo)
    server.register_function(join)
    
    server.serve()

def echo(self):
    return 'Hello world!'

def join(name):
    if name is None:
        name = 'cye'
        
    queue = TaskQueue.getInstance()
    queue.addTask(Task(name))
    return "rpc say: success! "

def usage():
    print "[usage] python pusher.py start|stop|restart"
    pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        opt = 'restart'
    else:
        opt = sys.argv[1]
        
    if opt in ['start', 'stop', 'restart']:
        cyedaemon = CyeDaemon()
        
        if opt == 'start':
            cyedaemon.start()
            cyedaemon.delpid()
        elif opt == 'stop':
            cyedaemon.stop()
        elif opt == 'restart':
            cyedaemon.restart()
        
    else:
        usage()

    