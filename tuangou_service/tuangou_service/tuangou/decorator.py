# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps

from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine import respcode, exception
from pylon.frame import make_response

from tuangou.api import request
from tuangou import settings


_LOGGER = logging.getLogger(__name__)


EXCEPTION_DEBUG = settings.EXCEPTION_DEBUG

EXCEPTION_CODE_PAIRS = (
    (respcode.AUTH_ERROR, exception.AuthFailureError,),
    (respcode.DB_ERROR, exception.DbError,),
    (respcode.DATA_ERROR, exception.DataError,),
    (respcode.DATA_ERROR, exception.UniqueCheckError,),
    (respcode.PARAM_ERROR, exception.ParamError,),
    (respcode.IO_ERROR, IOError,),
    (respcode.UNKNOWN_ERROR, exception.UnknownError,),
)


def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            req_h = request.headers
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            #h['Access-Control-Allow-Headers'] = 'true'
            h['Access-Control-Allow-Origin'] = req_h.get('Origin', '*')
            h['Access-Control-Allow-Credentials'] = 'true'
            return resp
        return decorated_function
    return decorator


def access_control(f):
    @wraps(f)
    @add_response_headers({'Access-Control-Allow-Origin': '*'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


def _get_respcode_of_exception(e):
    e_type = type(e)
    for code, exception_type in EXCEPTION_CODE_PAIRS:
        if e_type == exception_type:
            return code
    else:
        return respcode.UNKNOWN_ERROR


def check_session(func):
    '''
    check user session
    '''
    @wraps(func)
    def wrapper(*args, **kv):
        cookies = request.cookies
        return func(*args, **kv)
    return wrapper


def exception_handler(func):
    """
    catch the exception and return specified respcode
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if request.method == 'OPTIONS':
                return json_response_ok({}, 'can cross-domain')
            return func(*args, **kwargs)
        except Exception as e:
            _LOGGER.exception(e)
            if EXCEPTION_DEBUG:
                raise e
            else:
                respcode = _get_respcode_of_exception(e)
                return json_response_error(respcode, e.message)
    return wrapper


def perf_logging(func):
    """
    Record the performance of each method call.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        fname = func.func_name
        msg = '%s -> %s' % (fname, ','.join('%s=%s' %
                                            entry for entry in zip(argnames, args) + kwargs.items()))
        try:
            start_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            proc_time = round(end_time - start_time, 3)
            _LOGGER.info('%s <- %s s.' % (msg, proc_time))
        except Exception as e:
            end_time = time.time()
            proc_time = round(end_time - start_time, 3)
            _LOGGER.error('%s error in %s s.' % (msg, proc_time))
            raise e
        return ret
    return wrapper
