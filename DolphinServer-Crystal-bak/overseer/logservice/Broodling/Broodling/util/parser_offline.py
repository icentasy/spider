import re
import json
from pyshm import shm_open, shm_write, shm_read
import datetime
import time
import sys
import os
import stat
import logging
from logging.handlers import RotatingFileHandler
from pymongo.connection import Connection
import subprocess
import MySQLdb

ONE_DAY = datetime.timedelta(days=1)
logger = logging.getLogger("Broodling LogParse")
# _mongo = Connection('127.0.0.1', 27017)['offline']
_mysql = MySQLdb.connect(host='10.190.45.121', user='dolphin',
                         passwd='dolphin_stat@logsvr', port=3306)


def init_log(log_path='./parse.log', maxB=10 * 1024 * 1024, bc=5, level=logging.INFO):
    Rthandler = RotatingFileHandler(
        log_path, maxBytes=int(maxB), backupCount=int(bc))
    formatter = logging.Formatter(
        '[%(process)d]%(asctime)s %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)
    logger.setLevel(int(level))
    logger.info("log init complete!")

init_log()


class ParseLog(object):
    MAX_READ_LINES = 100000

    def __init__(self, log_name, parser_list):
        self._file_path = None
        self._log_name = log_name
        self._fp = None
        self._inode = 0
        self._last_pos = 0
        self._last_parse_time = time.time()
        self._parser_list = []
        self._log_date = datetime.datetime.now()

        for parser_obj in parser_list:
            if parser_obj:
                self._parser_list.append(parser_obj)

    def set_file_record(self, file_path, inode, offset):
        if self._fp:
            self._fp.close()
            self._fp = None
        self._file_path = file_path

        self._inode = inode
        self._last_pos = offset

    def get_file_record(self):
        return (self._file_path, self._log_name, self._inode, self._last_pos)

    def show_state(self):
        for parser in self._parser_list:
            parser.show_state()

    def check(self):
        if not self._file_path or not self._log_name:
            logger.error("File path %s of %s was not initialed correctlly!"
                         % (self._file_path, self._log_name))
            return -1
        logger.debug("start parse %s in %s" %
                     (self._file_path, self._log_name))
        if not os.path.exists(self._file_path):
            logger.error("no exists file %s" % self._file_path)
            return -2

        try:
            file_stat = os.stat(self._file_path)
            if not stat.S_ISREG(file_stat.st_mode):
                logger.error("%s is not regular file" % self._file_path)
                return -2

            logger.debug("last inode:%d, last pos:%d" %
                         (self._inode, self._last_pos))
            if self._inode <= 0:
                self._inode = file_stat.st_ino
                self._last_pos = 0
                if self._fp:
                    self._fp.close()
                    self._fp = None
            elif self._inode != file_stat.st_ino:
                logger.info("File(%s)'s inode has been changed from %d to %d!"
                            % (self._file_path, self._inode, file_stat.st_ino))
                self._inode = file_stat.st_ino
                # here we can consider whether system archiving happened or someone remove the log, then do something appropriately
                # and now we just consider it system archiving
                self._last_pos = 0
                if self._fp:
                    self._fp.close()
                    self._fp = None
            if self._last_pos > file_stat.st_size:
                logger.info("File(%s)'s size has been changed from %d to %d!"
                            % (self._file_path, self._last_pos, file_stat.st_size))
                # here, may be system archiving happened or someone cut the
                # log, so the same as upstair.
                self._last_pos = 0
            elif self._last_pos < file_stat.st_size:
                # normal condition we come to here
                logger.debug("File(%s) size increase from %d to %d"
                             % (self._file_path, self._last_pos, file_stat.st_size))
                self.__read_content()
            elif self._last_pos == file_stat.st_size:
                logger.info('File(%s) read the end' % self._file_path)
                return -3

            return 0

        except Exception, e:
            logger.error("Exception accured during Check File %s! (%s)" %
                         (self._file_path, e))
            return -1

    def __read_content(self):
        if not self._fp:
            self._fp = open(self._file_path, 'r')

        line_count = 0
        self._fp.seek(self._last_pos)

        for line in self._fp:
            line_count += 1
            for parser in self._parser_list:
                (match, p_index) = parser.match(line)
                if match:
                    parser.parse_line(match, p_index)
                    break
            self._last_pos += len(line)
            if line_count >= ParseLog.MAX_READ_LINES:
                break


class ParserObject(object):

    def __init__(self, regex_list, shm_key=None, shm_size=102400):
        #self._shm_key = shm_key
        #self._shm_size = shm_size

        self._date_map = {}  # used to store data per date in shm
        # if self._shm_key:
        #    self.mount_shm(self._shm_key, self._shm_size)

        self._regex_pattern_list = []
        self.init_regex_pattern(regex_list)

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

    '''
    when new date comes, call this to submit yesterday's data, 
    usually insert to mysql. 
    then, clear the shared memory
    '''

    def submit_data(self):
        self.submit()
        # self.clear_shm()

    # when new day comes, we call this to submit the data of yesterday to mysql
    def submit(self):
        logger.info("submit data:%s" % self._date_map)
        print "submit data:%s" % self._date_map.get('site_map')

    '''
    mount the shared memory of SystemV 
    the shm_key and shm_size must be specified
    lastly, the date_map dict will be initialed for storage data in shm
    '''

    def mount_shm(self, shm_key, shm_size=102400):
        ret = shm_open(shm_key, shm_size)
        self._date_map = {}
        if ret == -1:
            print "[%s] get shared memory failed!" % self.__class__.__name__
            sys.exit(0)
        else:
            self._shm_key = shm_key
            self._shm_size = shm_size
            print "[%s] get shared memory succ!" % self.__class__.__name__
            shm_str = shm_read()
            print "%s read shm:%s" % (self.__class__.__name__, shm_str)
            if not shm_str:
                self._date_map = {}
            else:
                self._date_map = json.loads(shm_str)

    '''
    clear the shared memory
    '''

    def clear_shm(self):
        if self._shm_key:
            # clear the shm map
            ret = shm_open(self._shm_key, self._shm_size)
            shm_write('')

    '''
    when program received SIGTERM, call this to save current data to shm
    '''

    def destruct(self):
        if self._shm_key:
            print "[%s] catch term sinal, ready to save to shm..." % self.__class__.__name__
            new_shm_str = json.dumps(self._date_map)
            ret = shm_open(self._shm_key, self._shm_size)
            ret = shm_write(new_shm_str)
            if ret == -2:
                print "[%s] new shm str's size[%s] is too large!" % (self.__class__.__name__, len(new_shm_str))
            elif ret == -1:
                print "[%s] get shared memory failed!" % self.__class__.__name__
            else:
                print "[%s] save succ!" % self.__class__.__name__


class TestParser(ParserObject):

    def __init__(self, regex_str_list, shm_key=None, shm_size=102400):
        super(TestParser, self).__init__(regex_str_list, shm_key, shm_size)

    def parse_line(self, match, p_index=0):
        '''
            todo parse method
        '''
        # print match.groups()
        self._parsed_count = 0
        push_time = match.group(1)
        flag = match.group(2)  # flag for succ push or fail push
        if len(match.groups()) >= 8:
            user_id = int(match.group(3))
            src_did = match.group(4)
            dst_did = match.group(6)
            push_type = int(match.group(8))

        date_str = get_date_str(self._log_date)
        if not self._date_map.has_key(date_str):
            data_map = {}
            self._date_map[date_str] = data_map
        else:
            data_map = self._date_map[date_str]

        if flag == 'processTabPush':
            try:
                url = match.group(3)
                org_site = re.match(
                    r'.*?/{2}(.*?)/.*|.*?\\/\\/(.*?)\\/.*', url)
                if org_site:
                    site = org_site.group(1)
                    if not site:
                        site = org_site.group(2)
                    data_map[site] = data_map.get(site, 0) + 1
            except Exception, e:
                logger.debug(e)

    def submit_data(self, date_str, type_name):
        logger.info('offline output')
        # todo output
        # result = self._data_map
        # for i in result:
        #     tmp = {'site': i, 'count': result[i]}
        #     print tmp
        #     _mongo['%s_%s' % (type_name, date_str)].insert(tmp)

        # self._data_map = {}
        if hasattr(self, '_date_map'):
            for (date_str_tmp, data_map) in self._date_map.items():
                table_name = "Site_Statistics_" + date_str
                logger.info('Table_name :%s' % table_name)
                insert_sql = "insert into %s (site_url,\
                                           count,\
                                           api_type) values" % table_name
                sort_site_maps_list = sorted(
                    data_map.iteritems(), key=lambda d: d[1], reverse=True)
                sort_site_maps = {x: y for x, y in sort_site_maps_list[0:100]}
                insert_count = 0
                api_type = 2
                for (key, value) in sort_site_maps.items():
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s', %d, %d)" %\
                        (key,
                         value,
                         api_type)
                    insert_count += 1
                logger.info("[Site_Statistics]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
                print "Done"
            self._date_map = {}
        # print "submit data:%s"%self._date_map.get('site_map')


def get_date_str(date):
    year = str(date.year)
    month = str(date.month) if date.month > 9 else "0" + str(date.month)
    day = str(date.day) if date.day > 9 else "0" + str(date.day)
    date_str = '%s%s%s' % (year, month, day)
    return date_str


def reduce_date(now, interval):
    i = 0
    while(i < interval):
        now = now - ONE_DAY
        print now
        i += 1
    return now

'''
usage:
python test_parser_offline.py time_intever time_star service_type compress_log_name log_name

eg. python  test_parser_sync_top_site.py 5 2 dolphinsync-en/service-info info.log.lzo info.log
'''

if __name__ == "__main__":
    parser_list = []

    regex_str_list = [
        r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d),\d+ INFO \[org.dolphin.PushService\] - (processTabPush):.*?push_data.*?url":"(http.*?)"']
    parser = TestParser(regex_str_list, shm_key=None, shm_size=102400)
    parser_list.append(parser)

    log_reader = ParseLog('DolphinService', parser_list)
    #arglen = len(sys.argv) -1
    time_inter = int(sys.argv[1])
    time_start = int(sys.argv[2])
    service = sys.argv[3]
    lzo_name = sys.argv[4]
    file_name = sys.argv[5]
    i = 0
    parser_date = datetime.datetime.now()
    parser_date = reduce_date(parser_date, time_start)
    print parser_date
    while(i < time_inter):
        date_str = get_date_str(parser_date)
        subprocess.call('rm /mnt2/offline/%s' % file_name, shell=True)
        subprocess.call(
            's3cmd get -c "/home/ubuntu/.s3cfg" s3://logserver/input/%s/%s/%s /mnt2/offline/' %
            (service, date_str, lzo_name), shell=True)
        subprocess.call('lzop -d /mnt2/offline/%s' % lzo_name, shell=True)
        subprocess.call('rm /mnt2/offline/%s' % lzo_name, shell=True)
        log_reader.set_file_record('/mnt2/offline/%s' % file_name, 0, 0)
        while 1:
            ret = log_reader.check()
            if ret != 0:
                break

        for parser_obj in parser_list:
            print "in parser_list"
            parser_obj.submit_data(date_str, 'push_info')
        parser_date = parser_date - ONE_DAY
        i += 1
