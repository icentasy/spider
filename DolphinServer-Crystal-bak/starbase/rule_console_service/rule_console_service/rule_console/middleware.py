# -*- coding:utf-8 -*-
'''
just a test for middleware in pylon
'''
import logging

from pylon.frame import request
from rule_console.api import app


_LOGGER = logging.getLogger(__name__)


class TestMiddleware(object):
    @app.before_request
    def before_request():
        _LOGGER.info('remote ip:%s' % request.remote_addr)

    @app.teardown_appcontext
    def after_request(response):
        _LOGGER.debug('teardown...')
