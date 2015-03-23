# -*- coding: utf-8 -*-
import logging
from base import ModelBase

_LOGGER = logging.getLogger("model")


class Module(ModelBase):
    collection = 'modules'
    required = ('module_name', 'app_name', 'module_value', 'order')
    unique = ('model_name',)
    optional = ()
    params = set(['module_name', 'module_vaule', 'order'])

    @classmethod
    def new(
            cls, appname, module_name, module_value, order=1):
        '''
        create module instance
        '''
        instance = cls()
        instance.data = {}

        instance.data['module_name'] = module_name
        instance.data['app_name'] = appname
        instance.data['module_value'] = module_value
        instance.data['order'] = order
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data['_id'] = max_id
        return cls.insert(appname, instance.data)

    @classmethod
    def update_module(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_module(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_module(cls, appname, cond, fields={}):
        users = cls.find(appname, cond, fields, toarray=True)
        if users:
            return users[0]
        else:
            return None

    @classmethod
    def del_module(cls, appname, mid):
        return cls.remove(appname, {"_id": int(mid)})
