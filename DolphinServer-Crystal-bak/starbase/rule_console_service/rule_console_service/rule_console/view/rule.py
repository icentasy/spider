# -*- coding:utf-8 -*-
import logging


from rule_console.model.rule import Rule
from rule_console.model.refered_info import ReferInfo
from rule_console.model import ArmoryMongo
from armory.marine.util import now_timestamp, unixto_string
from rule_console import settings

_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT
_RULE_FILTER_KEY = ['package', 'locale']
#_RULE_DISPLAY_KEY = ['platform', 'package', 'operator', 'source', 'locale']
_RULE_DISPLAY_KEY = ['operator', 'source', 'locale']


def get_rule_filter_list(appname):
    filter_list = []
    sort = [("last_modified", -1)]
    for filter_item in _RULE_FILTER_KEY:
        filter_dict = {"items": [], "name": filter_item}
        filter_cursor = ArmoryMongo[appname][filter_item].find({}).sort(sort)
        for item in filter_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            filter_dict['items'].append(item_dict)
        if filter_item == "package":
            default = {"display_value": u"项目名称", "value": "all"}
        else:
            default = {"display_value": u"选择Locales", "value": "all"}
        filter_dict["items"].insert(0, default)
        filter_list.append(filter_dict)

    return filter_list


def get_rule_display_data(appname):
    display_data = {}
    sort = [("title", 1), ("_id", 1)]

    # get operator/source/locale info list
    for display_item in _RULE_DISPLAY_KEY:
        display_cursor = ArmoryMongo[appname][display_item].find(
            {}).sort(sort)
        display_list = []
        for item in display_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            display_list.append(item_dict)
        display_data[display_item] = display_list

    # get platform and package info linkage control dict
    fields = {"_id": 1, "title": 1}
    info = {"name": "platform", "items": []}
    platform_cursor = ArmoryMongo[appname]["platform"].find(
        {}, fields).sort(sort)
    for os_item in platform_cursor:
        plat_dict = {"display_value": "", "value": "", "children": {}}
        plat_dict["value"] = os_item.get("_id")
        plat_dict["display_value"] = os_item.get("title")
        plat_child = {"name": "package", "items": []}
        cond = {"platform": os_item["_id"]}
        package_cursor = ArmoryMongo[appname]["package"].find(
            cond, fields).sort(sort)
        for item in package_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            plat_child["items"].append(item_dict)
        plat_dict["children"] = plat_child
        info["items"].append(plat_dict)
    display_data["platform"] = info

    return display_data


def rule_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    rule = []
    rule_cursor = Rule.find_rule(appname, cond, fields)
    if sort is not None:
        rule_cursor = rule_cursor.sort(sort)
    rule_cursor = rule_cursor.skip(
        page * page_size).limit(page_size)
    total = Rule.find_rule(appname, cond).count()
    for item in rule_cursor:
        item["id"] = item.pop("_id")
        item["first_created"] = unixto_string(item.get("first_created"))
        item["last_modified"] = unixto_string(item.get("last_modified"))
        rule.append(item)
    data = {}
    data.setdefault("items", rule)
    data.setdefault("total", total)
    return data


def save_rule_info(appname, rule_dict):
    for arg in ["package", "operator", "source", "locale"]:
        rule_dict[arg] = [int(i) for i in rule_dict[arg]]
    rule_instance = Rule.new(rule_dict)
    Rule.save_rule(appname, rule_instance)
    _LOGGER.info("add a new rule:%s", rule_dict["title"])


def get_rule_by_id(appname, pid, fields=None):
    rule_id = int(pid)
    cond = {"_id": rule_id}
    rule_info = Rule.find_one_rule(appname, cond, fields)
    rule_info["id"] = rule_info.pop("_id")
    return rule_info


def update_rule_info(appname, pid, data):
    cond = {"_id": pid}
    data["last_modified"] = now_timestamp()
    for arg in ["package", "operator", "source", "locale"]:
        data[arg] = [int(i) for i in data[arg]]
    if data.get("id"):
        data.pop("id")
    Rule.update_rule(appname, cond, data)
    _LOGGER.info("update locale:%s success", pid)
    return get_rule_by_id(appname, pid)


def delete_rule_info(appname, rule_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for rule_id in rule_ids:
        cond = {"_id": int(rule_id)}
        rule = Rule.find_one_rule(appname, cond, None)
        if rule:
            refer_cond = {"target_id": int(rule_id), "target_field": "rule"}
            refer_rule = ReferInfo.find_one_refered_info(
                appname, refer_cond, None)
            if refer_rule:
                _LOGGER.info("rule id %s is refer" % rule_id)
                refer_info = {"id": rule_id}
                refer_info["refered_info"] = refer_rule["refered_info"]
                refered_ids.append(refer_info)
            else:
                Rule.del_rule(appname, rule_id)
                success_ids.append({"id": rule_id})
        else:
            _LOGGER.info("rule id %s is not exist" % rule_id)
            invalid_ids.append(rule_id)
    return success_ids, refered_ids, invalid_ids
