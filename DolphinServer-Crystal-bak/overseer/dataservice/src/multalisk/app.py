# -*- coding:utf-8 -*-
"""
    multalisk.app
    ~~~~~~~~~~~~~

    This model implements the central report application object.

"""
from pylon.frame import App, request, Blueprint

from multalisk.model import init_model
from multalisk.model.base import MetaSQL, MetaMongo, MetaHive
from multalisk.view.report import fetch_report
from multalisk.utils.common import get_valid_params
from multalisk.utils.constant import REPORT_PARAM
from multalisk.utils.http_json import json_response_ok
from multalisk.utils.exception import ParamError
from multalisk.decorator import (check_session, exception_handler,
                                 perf_logging, access_control)


DEFAULT_HTTP_HOST = '0.0.0.0'

DEFAULT_HTTP_PORT = 5000

DEFAULT_PROCESS_NUM = 4


class Multalisk(object):

    """Multalisk application class.
    Provides interface to create a multalisk application.
    `init_conf` must be called before calling `run`.
    """
    DEFAULT_BLUEPRINT_NAME = 'default_page'

    URL_PREFIX = '/multalisk'

    API_ENDPOINT = '/report/<view_id>'

    BLUEPRINTNAME_FORMAT = '{0}{1}'

    def __init__(self, app_name):
        self.app_name = app_name
        self.MetaSQL = MetaSQL
        self.MetaMongo = MetaMongo
        self.MetaHive = MetaHive
        self.app = App(app_name)

    def init_conf(self, app_conf, debug=False):
        """This function used to initial config by `app_conf`, the dict
        provided by top layer code.
        """
        self.model_conf = app_conf['model']
        self.view_conf = app_conf['view']
        self.DEBUG = debug
        init_model(self.model_conf, debug=self.DEBUG)
        self._register_report_api()

    def _register_report_api(self):
        """Private function, used to register the default api for report
        """
        blueprint = Blueprint(Multalisk.DEFAULT_BLUEPRINT_NAME, self.app_name,
                              url_prefix=Multalisk.URL_PREFIX)
        if not self.DEBUG:
            self.report = exception_handler(self.report)
        blueprint.add_url_rule(Multalisk.API_ENDPOINT,
                               methods=frozenset(['GET']),
                               view_func=self.report)
        self.app.register_blueprint(blueprint)

    def _next_blueprint_name(self, basename):
        """Returns the next name for a blueprint with the specified base name.

        For example, if `basename` is ``'personapi'`` and blueprints already
        exist with names ``'personapi0'``, ``'personapi1'``, and
        ``'personapi2'``, then this function would return ``'personapi3'``.

        """
        # blueprints is a dict whose keys are the names of the blueprints
        blueprints = self.app.blueprints
        existing = [name for name in blueprints if name.startswith(basename)]
        # if this is the first one...
        if not existing:
            next_number = 0
        else:
            # for brevity
            b = basename
            existing_numbers = [int(n.partition(b)[-1]) for n in existing]
            next_number = max(existing_numbers) + 1
        return Multalisk.BLUEPRINTNAME_FORMAT.format(basename, next_number)

    def create_api(self, api_path, methods, view_func):
        """This function used to add extend api for multalisk application
        `api_path`: the new api path without the part of api prefix
        `methods`: the http function supported by the new api, must be list
        `view_func`: the view function of the new api
        """
        # create new blueprint with different name from exists
        api_name = api_path.split('/')[-1]
        blueprintname = self._next_blueprint_name(api_name)
        blueprint = Blueprint(blueprintname,
                              self.app_name,
                              url_prefix=Multalisk.URL_PREFIX)
        # add url rule to blueprint
        api_endpoint = (api_path if api_path.startswith('/') else
                        '/{0}'.format(api_path))
        api_methods = frozenset(methods)
        blueprint.add_url_rule(api_endpoint,
                               methods=api_methods,
                               view_func=view_func)
        self.app.register_blueprint(blueprint)

    def run(self, host=DEFAULT_HTTP_HOST, port=DEFAULT_HTTP_PORT):
        """This function used to run the multalisk application by
        the http server inside of pylon.
        But we always startup the application by uwsgi which will be configed
        at the top layer but not int multalisk.
        """
        self.app.run(host=host, port=port,
                     processes=DEFAULT_PROCESS_NUM,
                     debug=self.DEBUG)

    @access_control
    @perf_logging
    @check_session
    def report(self, view_id):
        """report API.
        This API is used for fetch report data from multiple database,
        including mysql/hive/mongo.

        Request URL: api/mutalisk/report

        HTTP Method: GET

        Parameter:
            - app: view id, eg:1001  app id will be defined by different
                                     bussiness one app id is related to one or
                                     multiple Data Model defined in view_conf
            - q: query string, eg:
                 {"filters":[{"name":"user_name","val":"xshu","op":"like"}]}

        Return:
            {
                "status": 0,
                "msg": "",
                "data":{
                    "filters": {},
                    "items": [
                        {
                            "x_val": "20140101",
                            "y_val": {
                                "US": 80,
                                "CN": 20
                            }
                        },
                        {
                            ...
                        }
                        ...
                    ]
                }
            }
        """
        # check args
        args = get_valid_params(request.args, REPORT_PARAM)
        # view logic
        if view_id not in self.view_conf:
            raise ParamError('view id[%s] not configured!' % view_id)
        view_dict = self.view_conf[view_id]
        feature_list = fetch_report(view_dict, args['q'])
        return json_response_ok(feature_list)
