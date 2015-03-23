# -*- coding: utf-8 -*-
import multalisk
from demo.settings import DEBUG

from demo.conf.app_conf import APP_CONF


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)
