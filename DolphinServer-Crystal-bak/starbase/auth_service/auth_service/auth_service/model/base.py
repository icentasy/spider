# -*- coding: utf-8 -*-

import logging
from armory.tank.mongo import ArmoryMongo
from armory.tank.mongo import DESCENDING


_LOGGER = logging.getLogger(__name__)


class ModelBase(dict):

    def __getattr__(self, name):
        return self[name] if name in self else None

    def __setattr__(self, name, value):
        self[name] = value
    # !!!

    def __delattr__(self, name):
        del self[name]

    @classmethod
    def find(cls, appname, cond={}, fields={}, toarray=False):
        _db = ArmoryMongo[appname]
        if toarray:
            info = list(_db[cls.collection].find(cond, fields))
        else:
            info = _db[cls.collection].find(cond, fields)
        return info

    @classmethod
    def find_max_id(cls, appname):
        _db = ArmoryMongo[appname]
        max_art_id = _db[cls.collection].find_one(
            {}, sort=[('_id', DESCENDING)], fields={'_id': 1})
        if max_art_id:
            return max_art_id['_id']
        else:
            return 0

    @classmethod
    def insert(cls, appname, data):
        _db = ArmoryMongo[appname]
        _db[cls.collection].insert(data)

    @classmethod
    def update(cls, appname, cond, data, multi=False):
        _db = ArmoryMongo[appname]
        _db[cls.collection].update(cond, {'$set': data}, multi=multi)

    @classmethod
    def remove(cls, appname, cond):
        _db = ArmoryMongo[appname]
        _db[cls.collection].remove(cond)
