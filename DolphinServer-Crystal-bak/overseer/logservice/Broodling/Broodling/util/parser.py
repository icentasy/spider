'''
Created on Apr 11, 2011

@author: chzhong
'''
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError


class FreeConfigParser(SafeConfigParser):

    def _get(self, section, conv, option, default):
        return conv(self.get(section, option, default=default))

    def get(self, section, option, raw=False, vars=None, default=None):
        try:
            return SafeConfigParser.get(self, section, option, raw, vars)
        except (NoSectionError, NoOptionError), err:
            if default is not None:
                return default
            raise err

    def getint(self, section, option, default=None):
        return self._get(section, int, option, default)

    def getfloat(self, section, option, default=None):
        return self._get(section, float, option, default)

    def getboolean(self, section, option, default=None):
        try:
            return SafeConfigParser.getboolean(self, section, option)
        except (NoSectionError, NoOptionError), err:
            if default is not None:
                return default
            raise err
