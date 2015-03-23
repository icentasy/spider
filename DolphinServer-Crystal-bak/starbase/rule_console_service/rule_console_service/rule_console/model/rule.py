# -*- coding:utf-8 -*-
import logging


from rule_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")
_MAX_VERSION = 4294967295


class Rule(ModelBase):
    collection = 'rule'
    required = ('platform', 'title', 'package', 'operator', 'source', 'locale')
    unique = ('title', )
    optional = (
        ('first_created', now_timestamp), ('last_modified', now_timestamp))
    params = set(['title', ])
    search_fields = {
        "_id": {"data_type": "int"},
        "title": {"data_type": "string"},
        "min_version": {"data_type": "int"},
        "max_version": {"data_type": "int"}
    }

    @classmethod
    def new(cls, rule_dict):
        """
        creat source instance
        """
        instance = cls()
        instance.title = rule_dict["title"]
        instance.platform = rule_dict["platform"]
        instance.package = rule_dict["package"]
        instance.operator = rule_dict["operator"]
        instance.source = rule_dict["source"]
        instance.locale = rule_dict["locale"]
        instance.min_version = rule_dict["min_version"]
        instance.max_version = rule_dict["max_version"] if \
            rule_dict.get("max_version") else _MAX_VERSION
        instance.min_value = rule_dict["min_value"] if \
            rule_dict.get("min_value") else 0
        instance.max_value = rule_dict["max_value"] if \
            rule_dict.get("max_value") else 100
        instance.gray_start = rule_dict["gray_start"] if \
            rule_dict.get("gray_start") else 0
        instance.gray_scale = rule_dict["gray_scale"] if \
            rule_dict.get("gray_scale") else 100
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save_rule(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance["_id"] = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_rule(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_rule(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_rule(cls, appname, cond, fields={}):
        rules = cls.find(appname, cond, fields, toarray=True)
        if rules:
            return rules[0]
        else:
            return None

    @classmethod
    def del_rule(cls, appname, rule_id):
        cond = {}
        cond["_id"] = int(rule_id)
        return cls.remove(appname, cond)
