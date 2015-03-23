# -*- coding: utf-8 -*-
# from pylon.frame import request
from multalisk.utils.http_json import json_response_ok
from multalisk.decorator import (check_session, exception_handler,
                                 perf_logging, access_control)


@exception_handler
@access_control
@perf_logging
@check_session
def test_api():
    # check args
    # ...
    result = 'this is a example for extending multlisk api.'
    return json_response_ok(result)
