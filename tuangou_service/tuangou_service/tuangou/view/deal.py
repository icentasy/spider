# -*- coding:utf-8 -*-
import logging

from tuangou.model.deal import Deal
from tuangou.utils.common import schema_mapping
from tuangou import settings

_LOGGER = logging.getLogger(__name__)

DEFAULT_SIZE = 30

def get_deal_list(city, dealtype, args):
    deal_list = []
    try:
        query = Deal.query.filter(Deal.city == city and Deal.type == dealtype)
        page = args.get('page', 1)
        order = args.get('order', None)
        if order is not None:
            if order > 0:
                query = query.order_by((Deal.new_price).asc())
            else:
                query = query.order_by((Deal.new_price).desc())
        items = query.all()
        for item in items:
            deal_list.append(schema_mapping(item.__dict__))
    except Exception, e:
        print e
        _LOGGER.exception(e)
    total = len(items) / DEFAULT_SIZE if len(items) % DEFAULT_SIZE == 0 else len(items) / DEFAULT_SIZE + 1
    deal_list = deal_list[(page - 1) * DEFAULT_SIZE: page * DEFAULT_SIZE - 1]
    return {
        'total': total,
        'items': deal_list
    }
