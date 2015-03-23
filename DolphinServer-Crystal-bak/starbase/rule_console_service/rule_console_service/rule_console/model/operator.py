# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Operator(ModelBase):
    collection = 'operator'
    required = ('title', "code")
    unique = ('title',)
    optional = (
        ('first_created', now_timestamp),
        ('last_modified', now_timestamp)
    )
    params = set(['title'])
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"}
    }

    @classmethod
    def new(cls, title, code):
        """
        creat operator instance
        """
        instance = cls()
        instance.title = title
        instance.code = code
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save_operator(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_operator(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_operator(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_operator(cls, appname, cond, fields={}):
        operators = cls.find(appname, cond, fields, toarray=True)
        if operators:
            return operators[0]
        else:
            return None

    @classmethod
    def del_operator(cls, appname, op_id):
        cond = {}
        cond["_id"] = int(op_id)
        return cls.remove(appname, cond)
