# -*- coding: UTF-8 -*-
import logging
import simplejson
from uuid import UUID
from decimal import Decimal
import pymongo
from bson.objectid import ObjectId

_LOGGER = logging.getLogger('armory')


class ArmoryJson(object):
    '''
    armory json lib, use this lib to json parser
    '''
    @staticmethod
    def encode(encode_dict):
        '''
        enocode json from python dict
        '''
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

        ret = _any(encode_dict)
        return simplejson.dumps(ret)

    @staticmethod
    def decode(decode_str):
        '''
        decode json from python dict
        '''
        if not isinstance(decode_str, str):
            _LOGGER.error('decode str err, decode parameter should be string')
            raise Exception('decode para err')
        return simplejson.loads(decode_str)


if __name__ == '__main__':
    rsp_dict = {}
    rsp_str = ''
    req_dict = '{"a":"b"}'
    rsp_dict = ArmoryJson.decode(req_dict)
    rsp_str = ArmoryJson.encode(rsp_dict)

