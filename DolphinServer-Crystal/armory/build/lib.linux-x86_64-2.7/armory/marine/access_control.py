# -*- coding: utf-8 -*-
import logging
from functools import wraps

from armory.marine.json_rsp import json_response_ok, json_response_error
from pylon.frame import request, make_response
from armory.marine.respcode import UNKNOWN_ERROR


_LOGGER = logging.getLogger('armory')


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
            h['Access-Control-Allow-Origin'] = req_h.get('Origin', '*')
            h['Access-Control-Allow-Credentials'] = 'true'
            accept_header = req_h.get('Access-Control-Request-Headers')
            if accept_header:
                h['Access-Control-Allow-Headers'] = accept_header
            return resp
        return decorated_function
    return decorator


def access_control(f):
    @wraps(f)
    @add_response_headers({'Access-Control-Allow-Origin': '*'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


def exception_handler(func):
    """
    catch the exception and return specified respcode
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if request.method == 'OPTIONS':
                return access_control(json_response_ok)({}, 'can cross-domain')
            return func(*args, **kwargs)
        except Exception as e:
            _LOGGER.exception(e)
            return json_response_error(UNKNOWN_ERROR)
    return wrapper
