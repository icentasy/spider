from flask import *


class App(Flask):

    def __init__(self, name, *args, **kw):
        super(App, self).__init__(name, *args, **kw)
