# -*- coding: utf-8 -*-
import logging
from base import ModelBase

_LOGGER = logging.getLogger("model")


class App(ModelBase):
    collection = 'apps'
    required = ('name', 'app_name', 'app_value', 'order')
    unique = ('name',)
    optional = ()
    params = set(['name', 'app_vaule', 'order'])

    @classmethod
    def new(cls, appname, name, app_value, order=1):
        '''
        create app instance
        '''
        instance = cls()
        instance.data = {}

        instance.data['name'] = name
        instance.data['app_name'] = appname
        instance.data['app_value'] = app_value
        instance.data['order'] = order
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data['_id'] = max_id
        return cls.insert(appname, instance.data)

    @classmethod
    def update_app(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_app(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_app(cls, appname, cond, fields={}):
        users = cls.find(appname, cond, fields, toarray=True)
        if users:
            return users[0]
        else:
            return None

    @classmethod
    def del_app(cls, appname, aid):
        cond = {}
        cond["_id"] = int(aid)
        return cls.remove(appname, cond)
