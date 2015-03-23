# -*- coding: UTF-8 -*-
import logging
import time
import threading

_LOGGER = logging.getLogger('armory')

lock = threading.Lock()


class ArmoryThread(threading.Thread):
    '''
    armory thread lib, use this lib to call multithread
    '''
    def __init__(self, threadName):
        super(ArmoryThread, self).__init__(name=threadName)

    def run(self):
        '''
        @you should rewrite this method to start thread
        '''
        pass


class ExThread(ArmoryThread):
    '''
    this is a thread inherit from armory thread
    '''
    def __init__(self, ExThreadName):
        super(ExThread, self).__init__(threadName=ExThreadName)

    def run(self):
        global lock
        while True:
            lock.acquire()
            print 'it works'
            lock.release()
            time.sleep(1)


if __name__ == '__main__':
    global lock
    a = ExThread('test')
    a.start()
    while True:
        lock.acquire()
        print 'it works main'
        lock.release()
        time.sleep(1)
