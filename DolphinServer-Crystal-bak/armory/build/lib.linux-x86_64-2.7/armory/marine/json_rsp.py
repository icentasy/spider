# -*- coding:utf-8 -*-
from __future__ import absolute_import
from armory.marine.json import ArmoryJson
from armory.marine.respcode import OK
from pylon.frame import make_response


def _json_response(status, data, msg=None):
    d = {'status': status, 'data': data, 'msg': msg}
    response = make_response(ArmoryJson.encode(d))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


def json_response_ok(data=None, msg=''):
    return _json_response(OK, data, msg)


def json_response_error(error_code, data=None, msg=''):
    return _json_response(status=error_code, data=data, msg=msg)


def json_request(request):
    return ArmoryJson.decode(request.raw_post_data)
