# -*- coding: utf-8 -*-
import logging
from armory.marine.util import now_timestamp
from base import ModelBase

_LOGGER = logging.getLogger("model")


class Group(ModelBase):
    collection = 'groups'
    required = ('group_name',)
    unique = ('group_name',)
    optional = (('permission_list', {}),)
    #params = set(['group_name', 'permission_list'])
    params = set(['group_name'])

    @classmethod
    def new(cls, group_name, permission_list={}):
        """
        creat group instance
        """
        instance = cls()
        instance.data = {}
        instance.data['group_name'] = group_name
        instance.data['permission_list'] = permission_list
        instance.data['modified'] = now_timestamp()
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data['_id'] = max_id
        return cls.insert(appname, instance.data)

    @classmethod
    def update_group(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_group(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_group(cls, appname, cond, fields={}, toarray=True):
        groups = cls.find(appname, cond, fields, toarray)
        if groups:
            return groups[0]
        else:
            return None

    @classmethod
    def del_group(cls, appname, gid):
        cond = {}
        cond["_id"] = int(gid)
        return cls.remove(appname, cond)
