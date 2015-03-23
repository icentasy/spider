# -*- coding: UTF-8 -*-
import logging
import socket

_LOGGER = logging.getLogger('armory')


class ArmoryTcp(object):
    '''
    armory tcp lib, use this lib to call tcp function
    '''
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        return self.sock.connect((ip, port))

    def recv(self, bufsize):
        return self.sock.recv(bufsize)

    def send(self, buff):
        return self.sock.send(buff)

    def __del__(self):
        self.sock.close()


class ArmoryUdp(object):
    '''
    armory tcp lib, use this lib to call tcp function
    '''
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, buff, ip, port):
        return self.sock.sendto(buff, (ip, port))

    def recv(self, buffsize):
        return self.sock.recvfrom(buffsize)
