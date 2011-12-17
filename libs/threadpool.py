# -*- coding: utf-8 -*-
'''
Created on 2011-12-3

@author: lixiaojun
'''
from libs.cyetools import logger
import Queue
import sys
import threading
import time


class TaskQueue(object):
    __instance = None
    __lock = threading.Lock()
    
    def __init__(self):
        pass

    @classmethod
    def getInstance(self):
        self.__lock.acquire()
        if not self.__instance:
            self.__instance = super(TaskQueue,self).__new__(self)
        self.__lock.release()
        
        return self.__instance

    def initQueue(self,task_queue_size = 100, timeout=5):
        self.tasks = Queue.Queue(task_queue_size)
        self.timeout = timeout
        logger.info('Initislize Task Queue. size is (%d)' % task_queue_size)

    def getTask(self):
        try:
            return self.tasks.get(0)
        except:
            raise Exception,'This queue is empty.'

    def addTask(self,task):
        try:
            self.tasks.put(task, 0)
            logger.info('New task join in, Current length of Queue [%d]' % self.tasks.qsize())
            print 'New task join in, Current length of Queue [%d]' % self.tasks.qsize()
        except:
            logger.error('The task queue is full.')
            raise Exception,'This queue is full.'
    pass

class BaseThread(threading.Thread):
    def __init__(self):
        super(BaseThread,self).__init__()

        self._e = threading.Event()
        self.setDaemon(True)
        self.isReady(True)
        self.isActive(True)

    def wait(self):  
        self.isReady(True)
        self._e.clear()
        self._e.wait()

    def proceed(self):
        self.isReady(False)
        self._e.set()
        
        if not self.isAlive() and self.isActive():
            self.start()

    def shutdown(self):
        self.isActive(False)

        if not self._e.isSet():
            self.proceed()

    def isReady(self,flag = None):
        if isinstance(flag,bool):
            self.is_ready = flag
    
        return self.is_ready

    def isActive(self,flag = None):
        if isinstance(flag,bool):
            self.is_active = flag
    
        return self.is_active
    
class TaskThread(BaseThread):
   
    def run(self):
        while self.isActive():
            try:
                logger.info('[%s] is working ' % self.getName())
                print '%s is working' % self.getName()
                self.task()
            except:
                pass
            finally:
                self.wait()

    def bindTask(self,task):
        self.task = task
        logger.debug('[%s] bind Task(%s)' % (self.getName(), self.task))

class ThreadPool(object):
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def getInstance(self):
        self.__lock.acquire()
        if not self.__instance:
            self.__instance = super(ThreadPool,self).__new__(self)
        self.__lock.release()
        
        return self.__instance

    def initPool(self,pool_min_size = 5,pool_max_size = 10):
        self.pool_min_size = pool_min_size
        self.pool_max_size = pool_max_size
        self.pool = []

        for i in range(self.pool_min_size):
            t = TaskThread()
            self.pool.append(t)
        logger.info('Initialize Thread Pool. min_size = %d, max_size = %d' % (self.pool_min_size, self.pool_max_size))

    def getThread(self):
        th = None
        i = 0
        
        self.__lock.acquire()
        for i,t in enumerate(self.pool):
            if not t._e.isSet() and t.isReady():
                t.isReady(False)
                th = t
                break
        self.__lock.release()

        if th is None and len(self.pool) < self.pool_min_size:
            th = TaskThread()
            self.pool.append(th)

        return i,th

    def getIdleThreadsAmount(self):
        i = 0

        for t in self.pool:
            if t.isReady():
                i += 1

        return i
    
class ThreadPoolManager(BaseThread):
    def __init__(self,pool,tasks):
        super(ThreadPoolManager,self).__init__()
       
        self.pool = pool
        self.tasks = tasks
        logger.info('ThreadPool Manager run.')
        
    def run(self):
        while self.isActive() or True:
            i,t = self.pool.getThread()
            if t is not None:
                try:
                    task = self.tasks.getTask()
                except:
                    t.isReady(True)
                    #print sys.exc_info()[:2]
                else:
                    t.bindTask(task)
                    t.proceed()
                    
class PollingThread(BaseThread):
    def __init__(self,timeout = 60):
        super(PollingThread,self).__init__()

        self.timeout = timeout

    def run(self):
        while self.isActive():
            time.sleep(self.timeout)
            self.doAction()

    def doAction(self):
        pass
    
class LoadBalancingThread(PollingThread):
    def __init__(self,timeout,pool):
        super(LoadBalancingThread,self).__init__(timeout)
        self.pool = pool

    def doAction(self):
        n = self.pool.getIdleThreadsAmount()
        min_size = self.pool.pool_min_size
        max_size = self.pool.pool_max_size

        size = 0

        if (max_size - min_size)/2 <= n:
            size = (max_size - min_size)/2
        elif min_size < n:
            size = n - min_size

        for k in range(size):
            i,t = self.pool.getThread()

            del self.pool.pool[i]
            t.shutdown()
