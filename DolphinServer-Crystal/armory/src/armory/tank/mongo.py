import pymongo
from pymongo import collection
try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient
from pymongo import database
try:
    from pymongo import MongoReplicaSetClient
except ImportError:
    from pymongo import ReplicaSetConnection as MongoReplicaSetClient
from pymongo import uri_parser
from pymongo import ReadPreference
from armory.marine.json import ArmoryJson

DESCENDING = pymongo.DESCENDING
"""Descending sort order."""

ASCENDING = pymongo.ASCENDING
"""Ascending sort order."""


class Meta(type):
    def __getitem__(self, route):
        return self.db(route)


class ArmoryMongoClient(MongoClient):

    def __getattr__(self, name):
        attr = super(ArmoryMongoClient, self).__getattr__(name)
        if isinstance(attr, database.Database):
            return Database(self, name)
        return attr


class ArmoryMongoReplicaSetClient(MongoReplicaSetClient):
    def __getattr__(self, name):
        attr = super(ArmoryMongoReplicaSetClient, self).__getattr__(name)
        if isinstance(attr, database.Database):
            return Database(self, name)
        return attr


class Database(database.Database):
    def __getattr__(self, name):
        attr = super(Database, self).__getattr__(name)
        if isinstance(attr, collection.Collection):
            return Collection(self, name)
        return attr


class Collection(collection.Collection):
    def __getattr__(self, name):
        attr = super(Collection, self).__getattr__(name)
        if isinstance(attr, collection.Collection):
            db = self._Collection__database
            return Collection(db, attr.name)
        return attr


class ArmoryMongo(object):
    __metaclass__ = Meta
    connection_dict = {}

    def __init__(self):
        pass

    @classmethod
    def init_app(cls, app):
        if 'pymongo' not in app.extensions:
            app.extensions['pymongo'] = {}
        config_uri = ArmoryJson.decode(app.config['mongodb_conf'])
        if not isinstance(config_uri, dict):
            raise Exception('mongodb config should be dict')
        for route in config_uri:
            if route not in app.extensions['pymongo']:
                (cx, db) = cls._init_conf(config_uri[route], route)
                app.extensions['pymongo'][route] = (cx, db)

    @classmethod
    def init_conf(cls, conf):
        if isinstance(conf, str):
            conf = ArmoryJson.decode(conf)
        if not isinstance(conf, dict):
            raise Exception('mongodb config should be dict')
        for route in conf:
            if route not in cls.connection_dict:
                (cx, db) = cls._init_conf(conf[route], route)

    @classmethod
    def _init_conf(cls, config_uri, route):
        '''
        config_uri should be like this:
        mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        '''
        parsed = uri_parser.parse_uri(config_uri)
        dbname = parsed['database']
        read_preference = parsed['options'].get('read_preference')
        auto_start_request = parsed['options'].get('auto_start_request', True)
        username = parsed['username']
        password = parsed['password']
        replica_set = parsed['options'].get('replica_set')
        max_pool_size = parsed['options'].get('max_pool_size')
        socket_timeout_ms = parsed['options'].get('socket_timeout_ms', None)
        connect_timeout_ms = parsed['options'].get('connect_timeout_ms', None)
        host = config_uri
        auth = (username, password)
        if any(auth) and not all(auth):
            raise Exception('Must set both USERNAME and PASSWORD or neither')
        if isinstance(read_preference, str):
            read_preference = getattr(ReadPreference, read_preference)
            if read_preference is None:
                raise ValueError(
                    'READ_PREFERENCE: No such read preference name')
            read_preference = read_preference
        args = [host]
        kwargs = {
            #'auto_start_request': auto_start_request,
            'tz_aware': True,
        }
        if read_preference is not None:
            kwargs['read_preference'] = read_preference
        if socket_timeout_ms is not None:
            kwargs['socketTimeoutMS'] = socket_timeout_ms

        if connect_timeout_ms is not None:
            kwargs['connectTimeoutMS'] = connect_timeout_ms

        if replica_set is not None:
            kwargs['replicaSet'] = replica_set
            connection_cls = ArmoryMongoReplicaSetClient
        else:
            connection_cls = ArmoryMongoClient
        if max_pool_size is not None:
            kwargs['max_pool_size'] = max_pool_size
        cx = connection_cls(*args, **kwargs)
        db = cx[dbname]
        if any(auth):
            db.authenticate(username, password)
        cls.connection_dict[route] = (cx, db)
        return (cx, db)

    @classmethod
    def cx(cls, route):
        if route not in cls.connection_dict:
            raise Exception('cant find route')
        return cls.connection_dict[route][0]

    @classmethod
    def db(cls, route):
        if route not in cls.connection_dict:
            raise Exception('cant find route')
        return cls.connection_dict[route][1]


if __name__ == '__main__':
    conf = {'myroute': 'mongodb://127.0.0.1/test1'}
    ArmoryMongo.init_conf(conf)
    ArmoryMongo['myroute'].test2.insert({'hello': 'world'})
    print ArmoryMongo['myroute'].test2.find_one({'hello': 'world'})
