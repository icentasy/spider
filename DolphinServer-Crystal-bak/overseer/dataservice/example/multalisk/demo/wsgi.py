"""
    provide startup application for uwsgi.
    To startup application with uwsgi by conf as follows,

    [uwsgi]
    module = wsgi

    The command `uwsgi --ini uwsgi.cfg` can startup the uwsgi application.
"""
from run import app

application = app.app
