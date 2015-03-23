# -*- coding: utf-8 -*-
import sys
sys.path.append("../")

from multalisk.cache import init_cache

from model import app, news
from api.test import test_api


# extend api for multalisk
app.create_api('/test', ['GET'], test_api)

init_cache()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
