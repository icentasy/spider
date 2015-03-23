#!/usr/bin/env python
#coding:utf-8

'''''
author: gavingeng
date:   2012-01-18 18:15:13
'''
import socket
import sys
import traceback
import datetime
from datetime import *
import time

def main():
    pass

def sendMsg(msg):  
    try:  
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        sock.connect(('127.0.0.1', 514))
        sock.sendall(msg)  
        sock.close()  
    except Exception,e:  
        print traceback.print_exc(e)  
    
if __name__=='__main__':
    count = 0
    while count < 100:
        print "Write test syslog now ..."  
        msg="%s: test log at %s" % (datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d %H:%M:%s"))
        sendMsg(str(msg))
        time.sleep(1)
        count += 1
