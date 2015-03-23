# -*- coding:utf-8 -*-
import logging

from rule_console.model.locale import Locale
from rule_console.model.rule import Rule
from armory.marine.util import now_timestamp, unixto_string
from rule_console import settings


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT


def locale_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    locale = []
    locale_cursor = Locale.find_locale(appname, cond, fields)
    if sort is not None:
        locale_cursor = locale_cursor.sort(sort)
    locale_cursor = locale_cursor.skip(
        page * page_size).limit(page_size)
    total = Locale.find_locale(appname, cond).count()
    for item in locale_cursor:
        item["id"] = item.pop("_id")
        item["first_created"] = unixto_string(item.get("first_created"))
        item["last_modified"] = unixto_string(item.get("last_modified"))
        locale.append(item)
    data = {}
    data.setdefault("items", locale)
    data.setdefault("total", total)
    return data


def save_locale_info(appname, title):
    locale_instance = Locale.new(title)
    Locale.save_locale(appname, locale_instance)
    _LOGGER.info("add a new locale:%s", title)


def get_locale_by_id(appname, pid, fields=None):
    locale_id = int(pid)
    cond = {"_id": locale_id}
    locale_info = Locale.find_one_locale(appname, cond, fields)
    locale_info["id"] = locale_info.pop("_id")
    return locale_info


def update_locale_info(appname, pid, data):
    cond = {"_id": pid}
    data["last_modified"] = now_timestamp()
    Locale.update_locale(appname, cond, data)
    _LOGGER.info("update locale:%s success", pid)
    return get_locale_by_id(appname, pid)


def delete_locale_info(appname, lc_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for lc_id in lc_ids:
        cond = {}
        cond["_id"] = int(lc_id)
        locale = Locale.find_one_locale(appname, cond, None)
        if locale:
            refer_cond = {}
            refer_cond["locale"] = int(lc_id)
            refer_rule = Rule.find_rule(
                appname, refer_cond, toarray=True)
            if refer_rule:
                _LOGGER.info("locale id %s is refer" % lc_id)
                refer_info = {"id":  lc_id, "refered_info": []}
                for item in refer_rule:
                    temp_dict = {"modelName": "rule"}
                    temp_dict["id"] = item.get("_id")
                    refer_info["refered_info"].append(temp_dict)
                refered_ids.append(refer_info)
            else:
                Locale.del_locale(appname, lc_id)
                success_ids.append({"id": lc_id})
        else:
            _LOGGER.info("locale id %s is not exist" % lc_id)
            invalid_ids.append(lc_id)
    return success_ids, refered_ids, invalid_ids
