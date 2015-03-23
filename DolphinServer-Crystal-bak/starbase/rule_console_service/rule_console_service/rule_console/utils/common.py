# -*- coding: utf-8 -*-
import logging
import re

_LOGGER = logging.getLogger(__name__)


def search_cond(search_keyword, search_fields):
    cond = {}
    regex_cond_list = []
    for key in search_fields.keys():
        regex_cond = {}
        if search_fields.get(key)["data_type"] == "int":
            try:
                regex_cond[key] = int(search_keyword)
            except:
                _LOGGER.info("not a number string")
        elif search_fields.get(key)["data_type"] == "string":
            regex_cond[key] = {"$regex": re.escape(search_keyword)}
        if regex_cond:
            regex_cond_list.append(regex_cond)
    if regex_cond_list:
        cond["$or"] = regex_cond_list
    return cond
