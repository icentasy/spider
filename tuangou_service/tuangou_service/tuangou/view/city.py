# -*- coding:utf-8 -*-
import logging

from tuangou.model.city import City
from tuangou.utils.common import schema_mapping
from tuangou import settings

_LOGGER = logging.getLogger(__name__)

DEFAULT_SIZE = 30

def get_city_list():
    city_list = []
    try:
        query = City.query.filter()
        items = query.all()
        for item in items:
            city_list.append(schema_mapping(item.__dict__))
    except Exception, e:
        print e
        _LOGGER.exception(e)
    return city_list