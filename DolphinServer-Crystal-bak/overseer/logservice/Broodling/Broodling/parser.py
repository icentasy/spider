import re
from util.util_log import logger
from util.util_common import get_today, get_date_str
from util.model import EventID, ApiType
import sys
import socket
import simplejson as json
try:
    from django.contrib.gis.geoip import GeoIP
except Exception, e:
    from django.contrib.gis.utils import GeoIP

from setting import FLUME_IP, FLUME_PORT
#from genpy.flume.ttypes import ThriftFlumeEvent
#from pyflume import FlumeClient


class ParserObject(object):

    def __init__(self, event_list, regex_list):
        self._log_date = get_today()
        self._event_list = event_list
        self._regex_pattern_list = []
        self._date_map = {}
        self.init_regex_pattern(regex_list)
        self.send_log = []
        print "FLUME_IP %s, FLUME_PORT %s" %(FLUME_IP, FLUME_PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update_log_date(self, log_date):
        self._log_date = log_date

    def init_regex_pattern(self, regex_list):
        for regex_str in regex_list:
            pattern = re.compile(regex_str)
            self._regex_pattern_list.append(pattern)

    '''
    one parser obj may have more than one regex pattern,
    so this function return match group and pattern index
    '''
    def match(self, line):
        if len(self._regex_pattern_list) == 0:
            return (None, None)
        p_index = 0
        for pattern in self._regex_pattern_list:
            regex_match = pattern.match(line)
            if regex_match:
                break
            p_index += 1
        return (regex_match, p_index)

    def parse_line(self, match, p_index):
        pass

    def submit_data(self):
        try:
#            logger.info("begin submmit data,%s", self.send_log[0])
            self.submit()
        except Exception, e:
            logger.error("Exception accured during parser %s submit! (%s)" %
                         (self.__class__.__name__, e))

    def submit(self):
        for single_log in self.send_log:
            print "Ohhhhhhhhhh, %s" % single_log
            self.sock.sendto(single_log, (FLUME_IP, int(FLUME_PORT)))
        self.send_log = []

    def destruct(self):
        pass

    @classmethod
    def new(cls):
        instance = cls()
        return instance


class News_weibo(ParserObject):
    regex_str_list = [r'.*?\[(.*?:.*?:.*?)\].*?weibo.json\?(.*?from=(.*?)&.*?wid=(.*?)&.*?)']

    def __init__(self):
        super(News_weibo, self).__init__(
            [EventID.News_weibo], News_weibo.regex_str_list)

    def parse_line(self, match, p_index=0):
        time = match.group(1)
        click_from = match.group(3)
        info = match.group(2)
        wid = match.group(4)
        regex_str = '.*?lc=(.*?)&.*?'
        m = re.match(regex_str, info)
        if m:
            lc = m.group(1)[0:5]
        else:
            lc = 'zh-cn'
        regex_str = '.*?feature=(.*?)&.*?'
        m = re.match(regex_str, info)
        if m:
            feature = m.group(1)
        else:
            feature = '0'
        if len(wid) > 16:
            wid = wid[0:16]
        single_log = '%s|%s|%s|%s|%s|%s\n' % (time, 'click', lc, click_from, feature, wid)
        self.send_log.append(single_log)
        self.submit_data()


class News_show(ParserObject):
    regex_str_list = [r'INFO (.*?),.*?(top|list|latest).json\?(.*?from=(.*?)&.*?ids=(.*?)) .*?']

    def __init__(self):
        super(News_show, self).__init__(
            [EventID.News_show], News_show.regex_str_list)

    def parse_line(self, match, p_index=0):
        time = match.group(1)
        info = match.group(3)
        source = match.group(4)
        wids = match.group(5).split(',')
        # get country
        regex_str = '.*?lc=(.*?)&.*?'
        m = re.match(regex_str, info)
        if m:
            lc = m.group(1)[0:5]
        else:
            lc = 'zh-cn'
        regex_str = '.*?feature=(.*?)&.*?'
        m = re.match(regex_str, info)
        if m:
            feature = m.group(1)
        else:
            feature = '0'
        single_log = '%s|%s|%s|%s|%s|%s\n' % (time, 'show', lc, source, feature, wids)
        self.send_log.append(single_log)
        self.submit_data()


class ParserFactory(object):

    @classmethod
    def new(cls, event_id):
        if event_id == EventID.News_weibo:
            print "create News weibo parser object ..."
            return News_weibo()
        elif event_id == EventID.News_show:
            print "create News show parser object ..."
            logger.info("get a show event")
            return News_show()
        else:
            return None
