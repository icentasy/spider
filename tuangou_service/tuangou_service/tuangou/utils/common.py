# -*- coding:utf-8 -*-
import logging

from tuangou.settings import PAGE_LIMIT
from tuangou.utils.constant import PARAM_OPTION_LIST

from armory.marine.respcode import PARAM_ERROR, UNKNOWN_ERROR
from armory.marine.exception import *


_LOGGER = logging.getLogger(__name__)


def schema_mapping(tran_dict):
    # del _sa_instance_state from sqlalchemy
    if '_sa_instance_state' in tran_dict:
        del tran_dict['_sa_instance_state']
    if 'city' in tran_dict:
        del tran_dict['city']
    if 'type_detail' in tran_dict:
        del tran_dict['type_detail']
    if 'invalid_time' in tran_dict:
        del tran_dict['invalid_time']
    return tran_dict


def get_offset_limit(query_dict):
    page = query_dict.get('page', 1)
    limit = query_dict.get('limit', PAGE_LIMIT)
    try:
        print page, limit
        page = int(page)
        assert page > 0
    except Exception as e:
        _LOGGER.exception(e)
        raise ParamError(e)
    offset = limit * (page - 1)
    return offset, limit


def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return (value.tzinfo is not None and
            value.tzinfo.utcoffset(value) is not None)


def _conv(func):
    '''
    internal func for converting data type
    '''
    def wrapper(*args, **kwargs):
        if func == bool:
            return bool(int(*args, **kwargs))
        return func(*args, **kwargs)
    return wrapper


def get_valid_params(query_dict, keys):
    '''
    get valid params by params rule
    '''
    try:
        result = {}
        for key in keys:
            paras = key.split('&')
            paras = paras[:4]
            (param_key, param_option,
             param_type, default_value) = tuple(paras) + (None,) * (4 - len(paras))
            if not param_key or param_option not in PARAM_OPTION_LIST:
                # invalid config for parameter %key%
                continue

            param_value = query_dict.get(param_key)

            if param_value is None:
                if param_option == 'need':
                    raise ParamError(param_key)
                if param_option == 'noneed':
                    continue
                if default_value is not None:
                    param_value = _conv(eval(param_type))(default_value)
                else:
                    param_value = default_value
            else:
                if param_type is not None:
                    try:
                        if param_type != 'str':
                            param_value = _conv(eval(param_type))(param_value)
                    except Exception as e:
                        raise ParamError(param_key)
            result[param_key] = param_value
        return result
    except Exception as e:
        _LOGGER.exception(e)
        if not isinstance(e, ParamError):
            raise UnknownError('get param error')
        else:
            _LOGGER.warn('check parameter exception![%s]' % e.msg)
            raise e
