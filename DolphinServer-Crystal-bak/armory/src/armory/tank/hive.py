# -*- coding: utf-8 -*-

import re
import sys
import logging

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

_LOGGER = logging.getLogger('armory')


class ArmoryHive(object):
    '''
    Access hive by hive_service and thrift
    '''
    __CONN_RE_Amazon = re.compile(
        r"(?P<Amazon>(?P<ip>ip[\-0-9]+)(?P<port>:[0-9]+)(?P<db>/[a-zA-Z]+.*[a-zA-Z0-9]$))", re.IGNORECASE)

    __CONN_RE_Internal = re.compile(
        r"(?P<Internal>(?P<ip>[0-9\.]+[0-9]+)(?P<port>:[0-9]+)(?P<db>/[a-zA-Z]+.*[a-zA-Z0-9]$))", re.IGNORECASE)

    def __init__(self, conf="hive://ip-10-143-212-90:10000/click_db"):
        '''
        conf on Amazon host
            "hive://ip-10-143-212-90:10000/click_db"
            parse it will get: hive_ip='ip-10-143-212-90', hive_port=10000, db_name = 'click_db'
        conf on Alibaba host:
            need to make sure about it
        conf on Internal host:
            "hive://54.83.7.16:10000/click_db"
            parse it will get: hive_ip='54.83.7.16', hive_port=10000, db_name = 'click_db'
        '''
        conf_re = None
        if conf.startswith('hive://ip-'):
            conf_re = self.__CONN_RE_Amazon
        else:
            conf_re = self.__CONN_RE_Internal

        try:
            m = conf_re.search(conf)
            self.hive_ip = m.group('ip')
            self.hive_port = int(m.group('port')[1:])
            self.db_name = m.group('db')[1:]

            transport = TSocket.TSocket(self.hive_ip, self.hive_port)
            self.transport = TTransport.TBufferedTransport(transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

            self.client = ThriftHive.Client(self.protocol)
        except Exception, e:
            _LOGGER.error("hive data access object construct error. Error=%s" % e)
        _LOGGER.debug("hive data access object construct success !")

    def getDbName(self):
        return self.db_name

    def hiveOpen(self):
        try:
            self.transport.open()
            self.hiveExecute("use %s" % self.getDbName())
        except Exception, e:
            _LOGGER.error("hive data access object open error. Error=%s" % e)
        _LOGGER.debug("hive data access object open success !")

    def hiveExecute(self, sql):
        try:
            self.client.execute(sql)
            result = self.client.fetchAll()
            _LOGGER.debug("hive query success !")
            return result
        except Exception, e:
            _LOGGER.error("hive data access object open error. Error=%s" % e)

    def hiveClose(self):
        self.transport.close()


if __name__ == '__main__':
    testHive = ArmoryHive('hive://54.83.7.16:10000/click_db')
    testHive.hiveOpen()
    print testHive.hiveExecute("show databases")
    print testHive.hiveExecute("desc monitor")
    print testHive.hiveExecute("select * from monitor limit 10")
    print testHive.hiveExecute("select * from monitor where scol = 'zh-cn'")
    testHive.hiveClose()
