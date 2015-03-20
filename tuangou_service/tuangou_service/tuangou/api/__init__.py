# -*- coding: utf-8 -*-
from pylon.frame import App, request
from tuangou.settings import MYSQL_CONFIG


app = App(__name__)
app.config['db'] = MYSQL_CONFIG
