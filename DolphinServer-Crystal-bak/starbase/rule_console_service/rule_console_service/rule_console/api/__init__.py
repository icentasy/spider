# -*- coding: utf-8 -*-
from pylon.frame import App, request
from rule_console.settings import MONGO_CONFIG


app = App(__name__)
app.config['mongodb_conf'] = MONGO_CONFIG
