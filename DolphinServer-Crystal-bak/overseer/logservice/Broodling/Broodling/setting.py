from util.parser import FreeConfigParser
import simplejson
import os


###Config Initial Start###
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
print "ROOT_PATH %s" % ROOT_PATH
cp = FreeConfigParser()
cp.read([os.path.join(ROOT_PATH, "conf/parse_log.cfg")])

LOG_PATH = cp.get('log', 'log_path')
MAX_BYTES = cp.get('log', 'max_bytes')
BACK_COUNT = cp.get('log', 'bc')
LOG_LEVEL = cp.get('log', 'level')

rule_str = cp.get('statistics', 'rule_str')
RULE_MAP = simplejson.loads(rule_str)

POLL_LIST = simplejson.loads(cp.get('statistics', 'poll_list'))

LOG_RECORD_FILE = cp.get('statistics', 'record_file')

SERVICE_IP = cp.get('statistics', 'service_ip')

# worker section
WORKER_LOG_PATH = cp.get('worker', 'log_path')
WORKER_MAX_BYTES = cp.get('worker', 'max_bytes')
WORKER_BACK_COUNT = cp.get('worker', 'bc')
WORKER_LOG_LEVEL = cp.get('worker', 'level')

WORKER_LIST = simplejson.loads(cp.get('worker', 'worker_list'))

FLUME_IP = cp.get('flume', 'host')
FLUME_PORT = cp.get('flume', 'port')

###Config Initial End###
