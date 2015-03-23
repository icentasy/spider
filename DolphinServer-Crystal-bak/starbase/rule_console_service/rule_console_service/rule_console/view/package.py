# -*- coding:utf-8 -*-
import logging

from rule_console.model import ArmoryMongo
from rule_console.model.rule import Rule
from rule_console.model.package import Package
from armory.marine.util import now_timestamp, unixto_string
from rule_console import settings


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT


def package_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    package = []
    package_cursor = Package.find_package(appname, cond, fields)
    if sort is not None:
        package_cursor = package_cursor.sort(sort)
    package_cursor = package_cursor.skip(
        page * page_size).limit(page_size)
    total = Package.find_package(appname, cond).count()
    for item in package_cursor:
        item["id"] = item.pop("_id")
        item["first_created"] = unixto_string(item.get("first_created"))
        item["last_modified"] = unixto_string(item.get("last_modified"))
        package.append(item)
    data = {}
    data.setdefault("items", package)
    data.setdefault("total", total)
    return data


def save_package_info(appname, title, platform, package_name):
    package_instance = Package.new(title, platform, package_name)
    Package.save_package(appname, package_instance)
    _LOGGER.info("add a new package:%s", title)


def get_package_by_id(appname, pid, fields=None):
    package_id = int(pid)
    cond = {"_id": package_id}
    package_info = Package.find_one_package(appname, cond, fields)
    package_info["id"] = package_info.pop("_id")
    return package_info


def update_package_info(appname, pid, data):
    cond = {"_id": pid}
    data["last_modified"] = now_timestamp()
    Package.update_package(appname, cond, data)
    _LOGGER.info("update package:%s success", pid)
    return get_package_by_id(appname, pid)


def delete_package_info(appname, pn_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for pn_id in pn_ids:
        cond = {}
        cond["_id"] = int(pn_id)
        locale = Package.find_one_package(appname, cond, None)
        if locale:
            refer_cond = {}
            refer_cond["package"] = int(pn_id)
            refer_rule = Rule.find_rule(
                appname, refer_cond, toarray=True)
            if refer_rule:
                _LOGGER.info("package id %s is refer" % pn_id)
                refer_info = {"id":  pn_id, "refered_info": []}
                for item in refer_rule:
                    temp_dict = {"modelName": "rule"}
                    temp_dict["id"] = item.get("_id")
                    refer_info["refered_info"].append(temp_dict)
                refered_ids.append(refer_info)
            else:
                Package.del_package(appname, pn_id)
                success_ids.append({"id": pn_id})
        else:
            _LOGGER.info("package id %s is not exist" % pn_id)
            invalid_ids.append(pn_id)
    return success_ids, refered_ids, invalid_ids


def get_package_display_data(appname):
    display_data = {}
    sort = [("last_modified", -1)]
    display_cursor = ArmoryMongo[appname]["platform"].find({}).sort(sort)
    display_list = []
    for item in display_cursor:
        item_dict = {}
        item_dict["display_value"] = item.get("title")
        item_dict["value"] = item.get("_id")
        display_list.append(item_dict)
    display_data["platform"] = display_list

    return display_data
