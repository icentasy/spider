# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase


_LOGGER = logging.getLogger("model")
_MAX_VERSION = 4294967295


class ReferInfo(ModelBase):
    collection = 'refered_info'
    required = ('target_field', 'target_id', "refered_infp")
    unique = ()
    optional = ()

    @classmethod
    def new(cls, target_field, target_id, refered_info):
        """
        creat refered instance
        """
        instance = cls()
        instance.target_field = target_field
        instance.target_id = target_id
        instance.refered_info = refered_info
        return instance

    @classmethod
    def save_refered_info(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance["_id"] = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_refered_info(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_refered_info(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_refered_info(cls, appname, cond, fields=None):
        rules = cls.find(appname, cond, fields, toarray=True)
        if rules:
            return rules[0]
        else:
            return None

    @classmethod
    def del_refered_info(cls, appname, info_id):
        cond = {}
        cond["target_id"] = int(info_id)
        return cls.remove(appname, cond)
