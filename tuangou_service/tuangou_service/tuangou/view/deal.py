# -*- coding:utf-8 -*-
import logging

from tuangou.model.deal import Deal
from tuangou.utils.common import schema_mapping
from tuangou import settings
from tuangou.mongo.base import get

# from tuangou.settings import STOPWORD

_LOGGER = logging.getLogger(__name__)

DEFAULT_SIZE = 30

def get_deal_list(city, dealtype, args):
    deal_list = []
    try:
        query = Deal.query.filter(Deal.city == city and Deal.type == dealtype)
        page = args.get('page', 1)
        order = args.get('order', None)
        q = args.get('q', None)
        q_set = None
        if order is not None:
            if order > 0:
                query = query.order_by((Deal.new_price).asc())
            else:
                query = query.order_by((Deal.new_price).desc())
        items = query.all()

        '''
        if q is not null
        '''
        if q:
            q_set = set()
            from tuangou.mmseg import mmseg
            mmseg.dict_load_defaults()
            algor = mmseg.Algorithm(q.encode('utf8'))
            for tok in algor:
                res = get("index", {"key": tok.text})
                if res:
                    res = res.get('arrays', [])
                else:
                    continue
                if q_set:
                    q_set = q_set.intersection(set(res))
                else:
                    q_set = set(res)
            print q_set


        for item in items:
            if(q_set is None or (q_set != set() and item.id in q_set)):
                deal_list.append(schema_mapping(item.__dict__))
    except Exception, e:
        print e
        _LOGGER.exception(e)
    total = len(deal_list) / DEFAULT_SIZE if len(deal_list) % DEFAULT_SIZE == 0 else len(deal_list) / DEFAULT_SIZE + 1
    deal_list = deal_list[(page - 1) * DEFAULT_SIZE: page * DEFAULT_SIZE - 1]
    return {
        'total': total,
        'items': deal_list
    }
