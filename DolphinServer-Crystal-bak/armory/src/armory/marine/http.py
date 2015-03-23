# -*- coding: UTF-8 -*-
import logging
import requests

_LOGGER = logging.getLogger('armory')


class ArmoryHttp(object):
    '''
    armory http lib, use this lib to call http get
    post https for network request
    '''

    def __init__(self, url, method, req_dict):
        '''
        init http client.
        Parameters:
            -method: get/post
            -req_dict: request dict
        '''
        if method != 'get' and method != 'post':
            _LOGGER.error('method err, method should be get/post')
            raise ValueError('http method should be get/post')
        if not isinstance(req_dict, dict):
            _LOGGER.error('req_dict err, req_dict should be dict')
            raise ValueError('http req para should be dict')
        if not isinstance(url, str) or not url.startswith('http'):
            _LOGGER.error('url err, should be string and start with http')
            raise ValueError('http req url should be string')
        self.method = method
        self.url = url
        self.req_dict = req_dict

    def get_url(self):
        '''
        get http(s) rsp
        '''
        rsp = {}
        try:
            if self.method == 'get':
                r = requests.get(self.url, params=self.req_dict)
            elif self.method == 'post':
                r = requests.post(self.url, data=self.req_dict)
            rsp['status_code'] = r.status_code
            rsp['text'] = r.text
            rsp['json'] = r.json()
        except Exception as e:
            _LOGGER.error(e)
            rsp['status_code'] = -1
        finally:
            return rsp


if __name__ == '__main__':
    my_http = ArmoryHttp('http://172.16.77.57:8088/google_review/view_comment', 'get', {'max_time': '2015-01-07','min_time': '2014-12-31'})
    result = my_http.get_url()
    print result['json']
