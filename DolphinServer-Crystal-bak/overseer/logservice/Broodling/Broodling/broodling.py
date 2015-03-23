# -*- coding: UTF-8 -*-
from util.util_xml import RecordXML
from util.util_log import logger, init_log
from util.util_common import init_time, get_date_str_ex, get_today, compare_date, is_update_time, is_file
from util.model import EventID
from parser import ParserFactory
import setting
from parse_log import ParseLog
import time
import signal

parse_log_list = []
parser_list = {}


def sig_term_handler(sig, func=None):
    logger.info("catch sig term...")
    for (event_id, parser_obj) in parser_list.items():
        print "desctruct event %s" % event_id
        parser_obj.destruct()

    for parse_log in parse_log_list:
        (file_path, log_date, log_type, inode,
         offset) = parse_log.get_file_record()
        logger.info("lastly update XML record, %s, inode:%s, offset:%s"
                    % (file_path, inode, offset))
        # update the record in xml by update interval
        record_xml.set_log_record(file_path, inode, offset)
    exit()


def init():
    init_time()
    init_log(setting.LOG_PATH,
             maxB=setting.MAX_BYTES,
             bc=setting.BACK_COUNT,
             level=setting.LOG_LEVEL)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, sig_term_handler)
    today = get_today()
    for event_id in EventID.EVENT_IDS:
        try:
            print "event_id:%d" % event_id
            parser_obj = ParserFactory.new(event_id)
            if parser_obj:
                parser_list[event_id] = parser_obj
                parser_obj.update_log_date(today)
            else:
                logger.error("wrong event id:%s" % event_id)
        except Exception, e:
            logger.error("wrong in new ParserFactory:%s" % e)
    update_logs(today)


def update_logs(date):
    global record_xml
    record_xml = RecordXML(setting.LOG_RECORD_FILE)
    date_str = get_date_str_ex(date)
    for (log_type, log_config) in setting.RULE_MAP.items():
        log_file = log_config["path"]
        log_file = log_file.replace('$DATE', date_str)
        (log_inode, log_off) = record_xml.get_log_record(log_file)
        logger.info("log file %s, log_inode %d", log_file, log_inode)
        tmp_parser_list = []
        for rule in log_config['rules']:
            event_id = rule['rule_id']
            if event_id in parser_list:
                tmp_parser_list.append(parser_list.get(event_id))
        new_parse_log = ParseLog(log_type, tmp_parser_list)
        new_parse_log.set_file_record(log_file, date, log_inode, log_off)
        print '%s %s %s-%s-%s' % (log_file, log_type, date.year, date.month, date.day)
        parse_log_list.append(new_parse_log)


def check_newdate_file():
    today = get_today()
    # check if new date comes for each log file
    for parse_log in parse_log_list:
        (file_path, log_date, log_type, inode,
         offset) = parse_log.get_file_record()
        if compare_date(today, log_date):
            old_date_str = get_date_str_ex(log_date)
            new_date_str = get_date_str_ex(today)
            new_file_path = file_path.replace(old_date_str, new_date_str)
            if is_file(new_file_path):
                # last time check the old log file then update mysql
                logger.info("last time to check the old file %s" % file_path)
                ret = parse_log.check()
                # update parse_log
                parse_log.set_file_record(new_file_path, today, 0, 0)
                # delete old xml node in xml file
                record_xml.delete_log_record(file_path)


def run():
    while True:
        # check time to update xml record /per one minute
        if is_update_time():
            update_record_flag = True
        else:
            update_record_flag = False
        check_newdate_file()
#        logger.info('----------run---------')
        today = get_today()
        for (event_id, parser_obj) in parser_list.items():
            parser_obj.update_log_date(today)
        # general logic, we come here usually
        for parse_log in parse_log_list:
            ret = parse_log.check()
            (file_path, log_date, log_type, inode,
             offset) = parse_log.get_file_record()
            if ret == 0:
                if update_record_flag:
                    logger.info("time to update XML record, %s, inode:%s, offset:%s"
                                % (file_path, inode, offset))
                    # show current state of parse log
                    parse_log.show_state()
                    # update the record in xml by update interval
                    record_xml.set_log_record(file_path, inode, offset)
            else:
                logger.info("%s check error!" % log_type)

        time.sleep(0.3)

if __name__ == "__main__":
    try:
        init()
        run()
    except Exception, e:
        for (event_id, parser_obj) in parser_list.items():
            print "desctruct event %s" % event_id
            parser_obj.destruct()

        for parse_log in parse_log_list:
            (file_path, log_date, log_type, inode,
             offset) = parse_log.get_file_record()
            logger.info("lastly update XML record, %s, inode:%s, offset:%s"
                        % (file_path, inode, offset))
            # update the record in xml by update interval
            record_xml.set_log_record(file_path, inode, offset)
            logger.error("Exception happen,%s" % e)