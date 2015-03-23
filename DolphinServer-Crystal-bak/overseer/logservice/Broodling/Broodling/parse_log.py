import os
import stat
from time import time
from util.util_log import logger


class ParseLog(object):
    MAX_READ_LINES = 1000

    def __init__(self, log_name, parser_list):
        self._file_path = None
        self._log_name = log_name
        self._fp = None
        self._inode = 0
        self._last_pos = 0
        self._last_parse_time = time()
        self._parser_list = []

        for parser_obj in parser_list:
            if parser_obj:
                self._parser_list.append(parser_obj)

    def set_file_record(self, file_path, log_date, inode, offset):
        if self._fp:
            self._fp.close()
            self._fp = None
        self._file_path = file_path
        self._log_date = log_date

        self._inode = inode
        self._last_pos = offset

    def get_file_record(self):
        return (self._file_path, self._log_date, self._log_name, self._inode, self._last_pos)

    def show_state(self):
        pass

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

            return 0

        except Exception, e:
            logger.error("Exception accured during Check File %s! (%s)" %
                         (self._file_path, e))
            return -3

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
