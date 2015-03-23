# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Package(ModelBase):
    collection = 'package'
    required = ('title', 'package_name', )
    unique = ('title',)
    optional = (
        ("first_created", now_timestamp), ("last_modified", now_timestamp))
    params = set(['title', 'package_name'])
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"},
        "package_name": {"data_type": "string"}
    }

    @classmethod
    def new(cls, title, platform,  package_name):
        """
        creat package instance
        """
        instance = cls()
        instance.title = title
        instance.platform = platform
        instance.package_name = package_name
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save_package(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_package(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_package(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray)

    @classmethod
    def find_one_package(cls, appname, cond, fields={}):
        packages = cls.find(appname, cond, fields, toarray=True)
        if packages:
            return packages[0]
        else:
            return None

    @classmethod
    def del_package(cls, appname, pn_id):
        cond = {}
        cond["_id"] = int(pn_id)
        return cls.remove(appname, cond)
