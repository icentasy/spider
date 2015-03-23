# -*- coding:utf-8 -*-
from __future__ import absolute_import

import json
import datetime
from uuid import UUID
from bson import ObjectId
from decimal import Decimal

from pylon.frame import make_response

from multalisk.utils.respcode import OK


DEBUG = True


class ArmoryJSONEncoder(json.JSONEncoder):

    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    (Copy from DjangoJSONEncoder, may be we can add it to Armory later)
    """

    def _is_aware(value):
        """
        Determines if a given datetime.datetime is aware.

        The logic is described in Python's docs:
        http://docs.python.org/library/datetime.html#datetime.tzinfo
        """
        return (value.tzinfo is not None and
                value.tzinfo.utcoffset(value) is not None)

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if ArmoryJSONEncoder._is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, Decimal):
            return str(o)
        else:
            return super(ArmoryJSONEncoder, self).default(o)


def json_encode(data):

    def _any(data):
        ret = None
        if isinstance(data, (list, tuple)):
            ret = _list(data)
        elif isinstance(data, UUID):
            ret = str(data)
        elif isinstance(data, dict):
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() can't handle Decimal
            ret = str(data)
        # here we need to encode the string as unicode
        # (otherwise we get utf-16 in the json-response)
        elif isinstance(data, str):
            ret = unicode(data, 'utf-8')
        elif isinstance(data, ObjectId):
            ret = str(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=ArmoryJSONEncoder, ensure_ascii=False,
                      indent=4 if DEBUG else 0)


def _json_response(status, data, msg=None):
    d = {'status': status, 'data': data, 'msg': msg}
    response = make_response(json_encode(d))
    response.headers['content_type'] = 'application/json; charset=utf-8'
    return response


def json_response_ok(data=None, msg=''):
    return _json_response(OK, data, msg)


def json_response_error(error_code, data=None, msg=''):
    return _json_response(status=error_code, data=data, msg=msg)


def json_request(request):
    return json.loads(request.raw_post_data)
