# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Locale(ModelBase):
    collection = 'locale'
    required = ('title', )
    unique = ('title',)
    optional = (
        ('first_created', now_timestamp),
        ('last_modified', now_timestamp)
    )
    params = set(['title', ])
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"}
    }

    @classmethod
    def new(cls, title):
        """
        creat locale instance
        """
        instance = cls()
        instance.title = title
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save_locale(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_locale(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_locale(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_locale(cls, appname, cond, fields={}):
        locales = cls.find(appname, cond, fields, toarray=True)
        if locales:
            return locales[0]
        else:
            return None

    @classmethod
    def del_locale(cls, appname, lc_id):
        cond = {}
        cond["_id"] = int(lc_id)
        return cls.remove(appname, cond)
