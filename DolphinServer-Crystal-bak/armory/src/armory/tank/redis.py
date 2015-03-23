# -*- coding: UTF-8 -*-
'''
redis lib & redis shard lib & redis lock
code from cloudSvr
'''
import logging
import time
import redis
import threading
import functools
from redis.sentinel import Sentinel

_LOGGER = logging.getLogger('armory')
_LOCK_TIMEOUT = 15


class ArmoryRedis(object):
    '''
    armory redis lib, use this lib to use redis cache
    '''
    def __init__(self, chost, cport, cpassword, cdbname):
        self.cache = redis.StrictRedis(host=chost,
                                       port=cport,
                                       password=cpassword,
                                       db=cdbname)

    def __wrap(self, method, *args, **kwargs):
        f = getattr(self.cache, method)
        return f(*args, **kwargs)

    def __getattr__(self, method):
        return functools.partial(self.__wrap, method)


'''
this func decorate a cache lock
'''
# lock_db = ArmoryRedis("localhost", 6379, "", 0)


def ar_cache_lock(func):

    def _wrap(lock_db, key, *args, **kwargs):
        lock = 0
        _LOCK_KEY = key
        while lock != 1:
            now_time = int(time.time())
            timestamp = now_time + _LOCK_TIMEOUT + 1
            expire_time = timestamp
            # try to get lock for identified shard_id and sync_type
            lock = lock_db.setnx(_LOCK_KEY, timestamp)
            if lock == 1:
                break
            else:
                out_time = lock_db.get(_LOCK_KEY)
                if out_time and now_time > int(out_time):
                    tmp_time = lock_db.getset(_LOCK_KEY, timestamp)
                    if not tmp_time or now_time > int(tmp_time):
                        break
            # sleep 10ms
            _LOGGER.info('got lock failed! try to sleep a while...')
            time.sleep(0.01)
        ret = func(key, *args, **kwargs)

        # try to release lock
        now_time = int(time.time())
        if now_time < expire_time:
            lock_db.delete(_LOCK_KEY)
        else:
            _LOGGER.error('job time out, \
                    lock has been aquired by other session')
        return ret

    return _wrap


class ArmoryShardRedis(ArmoryRedis):
    __instance = {}
    __lock = threading.Lock()

    def __init__(self):
        '''disable __init__ method '''

    def initConnection(self, confs):
        '''
        conf should be like this:
        [{"name":"redis_000","host":"10.67.174.105","port":26379,"db":0}, {"name":"redis_001", "host":"10.179.159.236", "port":26379,"db":0}]
        '''
        self.conns = {}
        self.enable = 1
        self.nodes = []
        try:
            host_port_list = [(d['host'], d['port']) for d in confs]
            sentinel = Sentinel(host_port_list, socket_timeout=0.3)
            for node_item in confs:
                node = node_item['name']
                self.nodes.append(node)
                conn = sentinel.master_for(node, db=confs[0]['db'],
                                           socket_timeout=0.3)
                if node in self.conns:
                    pass
                self.conns[node] = conn
        except Exception, e:
            _LOGGER.error("shard cache init connection error. Error=%s" % e)
        _LOGGER.debug("shard cache init connection, \
                 node length:%s" % len(self.nodes))

    def get_server(self, shard_key):
        return self.conns[self.nodes[shard_key / 10 % len(self.nodes)]]

    def __wrap(self, method, *args, **kwargs):
        try:
            if method in ['mget', ]:
                key = args[0][0]
            else:
                key = args[0]
            assert isinstance(key, basestring)
        except:
            raise ValueError("first argument must be sharding key")
        try:
            shard_key = int(key.split(":")[1])
        except:
            raise ValueError("key %s is not the right pattern. \
                    xxx:shardid:..." % key)
        server = self.get_server(shard_key)
        f = getattr(server, method)
        return f(*args, **kwargs)

    @staticmethod
    def getInstance(confs, server_nodes_name, store_type='armory'):
        ArmoryShardRedis.__lock.acquire()
        if store_type not in ArmoryShardRedis.__instance:
            instance = object.__new__(ArmoryShardRedis)
            object.__init__(instance)
            instance.initConnection(confs)
            ArmoryShardRedis.__instance[store_type] = instance
        ArmoryShardRedis.__lock.release()
        return ArmoryShardRedis.__instance[store_type]
