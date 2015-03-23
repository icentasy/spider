# -*- coding:utf-8 -*-
import logging


from rule_console.model.source import Source
from rule_console.model.rule import Rule
from armory.marine.util import now_timestamp, unixto_string
from rule_console import settings


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT


def source_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    source = []
    source_cursor = Source.find_source(appname, cond, fields)
    if sort is not None:
        source_cursor = source_cursor.sort(sort)
    source_cursor = source_cursor.skip(
        page * page_size).limit(page_size)
    total = Source.find_source(appname, cond).count()
    for item in source_cursor:
        item["id"] = item.pop("_id")
        item["first_created"] = unixto_string(item.get("first_created"))
        item["last_modified"] = unixto_string(item.get("last_modified"))
        source.append(item)
    data = {}
    data.setdefault("items", source)
    data.setdefault("total", total)
    return data


def save_source_info(appname, title):
    source_instance = Source.new(title)
    Source.save_source(appname, source_instance)
    _LOGGER.info("add a new source:%s", title)


def get_source_by_id(appname, sid, fields=None):
    source_id = int(sid)
    cond = {"_id": source_id}
    source_info = Source.find_one_source(appname, cond, fields)
    source_info["id"] = source_info.pop("_id")
    return source_info


def update_source_info(appname, pid, data):
    cond = {"_id": pid}
    data["last_modified"] = now_timestamp()
    Source.update_source(appname, cond, data)
    _LOGGER.info("update source:%s success", pid)
    return get_source_by_id(appname, pid)


def delete_source_info(appname, src_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for src_id in src_ids:
        cond = {"_id": int(src_id)}
        source = Source.find_one_source(appname, cond, None)
        if source:
            refer_cond = {}
            refer_cond["source"] = int(src_id)
            print "*******"
            print refer_cond
            refer_rule = Rule.find_rule(
                appname, refer_cond, toarray=True)
            if refer_rule:
                _LOGGER.info("source id %s is refer" % src_id)
                refer_info = {"id":  src_id, "refered_info": []}
                for item in refer_rule:
                    temp_dict = {"modelName": "rule"}
                    temp_dict["id"] = item.get("_id")
                    refer_info["refered_info"].append(temp_dict)
                refered_ids.append(refer_info)
            else:
                Source.del_source(appname, src_id)
                success_ids.append({"id": src_id})
        else:
            _LOGGER.info("source id %s is not exist" % src_id)
            invalid_ids.append(src_id)
    return success_ids, refered_ids, invalid_ids
