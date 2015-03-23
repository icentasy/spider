# -*- coding:utf-8 -*-
import logging

from rule_console.model.operator import Operator
from rule_console.model.rule import Rule
from armory.marine.util import now_timestamp, unixto_string
from rule_console import settings


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = 20
PAGE_SIZE = settings.PAGE_LIMIT


def operator_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    operator = []
    operator_cursor = Operator.find_operator(appname, cond, fields)
    if sort is not None:
        operator_cursor = operator_cursor.sort(sort)
    total = Operator.find_operator(appname, cond).count()
    operator_cursor = operator_cursor.skip(
        page * page_size).limit(page_size)
    for item in operator_cursor:
        item["id"] = item.pop("_id")
        item["first_created"] = unixto_string(item.get("first_created"))
        item["last_modified"] = unixto_string(item.get("last_modified"))
        operator.append(item)
    data = {}
    data.setdefault("items", operator)
    data.setdefault("total", total)
    return data


def save_operator_info(appname, title, code):
    operator_instance = Operator.new(title, code)
    Operator.save_operator(appname, operator_instance)
    _LOGGER.info("add a new operator:%s", title)


def get_operator_by_id(appname, oid, fields=None):
    operator_id = int(oid)
    cond = {"_id": operator_id}
    operator_info = Operator.find_one_operator(appname, cond, fields)
    operator_info["id"] = operator_info.pop("_id")
    return operator_info


def update_operator_info(appname, pid, data):
    cond = {"_id": pid}
    data["last_modified"] = now_timestamp()
    Operator.update_operator(appname, cond, data)
    _LOGGER.info("update operator:%s success", pid)
    return get_operator_by_id(appname, pid)


def delete_operator_info(appname, op_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for op_id in op_ids:
        cond = {}
        cond["_id"] = int(op_id)
        locale = Operator.find_one_operator(appname, cond, None)
        if locale:
            refer_cond = {}
            refer_cond["operator"] = int(op_id)
            refer_rule = Rule.find_rule(
                appname, refer_cond, toarray=True)
            if refer_rule:
                _LOGGER.info("operator id %s is refer" % op_id)
                refer_info = {"id":  op_id, "refered_info": []}
                for item in refer_rule:
                    temp_dict = {"modelName": "rule"}
                    temp_dict["id"] = item.get("_id")
                    refer_info["refered_info"].append(temp_dict)
                refered_ids.append(refer_info)
            else:
                Operator.del_operator(appname, op_id)
                success_ids.append({"id": op_id})
        else:
            _LOGGER.info("operator id %s is not exist" % op_id)
            invalid_ids.append(op_id)
    return success_ids, refered_ids, invalid_ids
