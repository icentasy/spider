"""
Settings and configuration for Dolphin Server Deploy Engine.

Ported from DJANGO 1.3.

Values will be read from the module specified by the DEPLOY_SETTINGS_MODULE environment
variable, and then from dolphindeploy.global_settings; see the global settings file for
a list of all possible variables.
"""

import os
import sys
import re
import time     # Needed for Windows
import warnings

from dolphindeploy import global_settings
from dolphindeploy import importlib


SETTINGS_MODULE_PATH = "conf/deploy_settings.py"

class BuildHandler(object):
    '''A abstract class that representing a pre-build phase.
    
    arguments:
        'includes':    A set of destinations to that should apply this handler.
        'excludes':    A set of destinations to that should not apply this handler.
        
        Destinations that in includes (if specified) and not in excludes (if specified) will be applied.
    '''

    def __init__(self, includes=None, excludes=None, **kwargs):
        self.includes = includes
        self.excludes = excludes

    def __call__(self, **kwargs):
        if self.should_handle(**kwargs):
            self.handle(**kwargs)

    def handle(self, **kwargs):
        raise NotImplemented()

    def should_handle(self, config_parser, **kwargs):
        confset = config_parser.defaults()['__confset__']
        if self.includes and confset not in self.includes:
            print "Skipping %s(not in %s)." % (confset, self.includes)
            return False
        if self.excludes and confset in self.excludes:
            print "Skipping %s(in excluded set %s)." % (confset, self.excludes)
            return False
        return True
class LazyObject(object):
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.

    By subclassing, you have the opportunity to intercept and alter the
    instantiation. If you don't need to do that, use SimpleLazyObject.
    """
    def __init__(self):
        self._wrapped = None

    def __getattr__(self, name):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is None:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is None:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        """
        Must be implemented by subclasses to initialise the wrapped object.
        """
        raise NotImplementedError

    # introspection support:
    __members__ = property(lambda self: self.__dir__())

    def __dir__(self):
        if self._wrapped is None:
            self._setup()
        return  dir(self._wrapped)

class LazySettings(LazyObject):
    """
    A lazy proxy for either global Django settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    Django uses the settings module pointed to by DJANGO_SETTINGS_MODULE.
    """
    def _setup(self):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        self._wrapped = Settings(SETTINGS_MODULE_PATH)

    def configure(self, default_settings=global_settings, **options):
        """
        Called to manually configure the settings. The 'default_settings'
        parameter sets where to retrieve any unspecified values from (its
        argument must support attribute access (__getattr__)).
        """
        if self._wrapped != None:
            raise RuntimeError('Settings already configured.')
        holder = UserSettingsHolder(default_settings)
        for name, value in options.items():
            setattr(holder, name, value)
        self._wrapped = holder

    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return bool(self._wrapped)
    configured = property(configured)

class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def safe_tuple(self, name):
        if hasattr(self, name):
            value = getattr(self, name)
            if not value:
                return ()
            if not isinstance(value, tuple):
                try:
                    value = tuple(value)
                except TypeError:
                    raise TypeError('"%s" canot be converted into a tuple.' % name)
            return value
        return ()

class Settings(BaseSettings):
    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        try:
            if os.path.exists(self.SETTINGS_MODULE):
                mod = importlib.import_file(self.SETTINGS_MODULE)
            elif self.SETTINGS_MODULE.endswith(".py"):
                print "Deploy settings file '%s' cannot be found." % self.SETTINGS_MODULE
                sys.exit(2)
            else:
                mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError, e:
            print "Could not import settings '%s' (Is it on sys.path?): %s" % (self.SETTINGS_MODULE, e)
            sys.exit(2)

        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

        if not self.PROJECT_NAME :
            raise KeyError('You must specify PROJECT_NAME in your settings file.')

        try:
            self.VERSION_CONTROL_MODULE = importlib.import_module(self.VERSION_CONTROL)
        except ImportError, e:
            raise ImportError("Could not import version control module '%s' (Is it on sys.path?): %s" % (self.VERSION_CONTROL, e))

        self.CONF_EXT_PATTERN = self.DEFAULT_CONF_EXT_PATTERN + self.safe_tuple('EXTRA_EXT_PATTERN')
        self.CONF_NAME_PATTERN = self.DEFAULT_CONF_NAME_PATTERN + self.safe_tuple('EXTRA_CONF_NAME_PATTERN')

        if not self.ROLE_APPS_TABLE :
            raise KeyError('ROLE_APPS_TABLE is None or empty. Have you forget to configure it?')

    def ensure_build_handlers(self):
        if hasattr(self, 'BUILD_HANDLERS'):
            return self.BUILD_HANDLERS
        return self.load_build_handlers()

    def load_build_handlers(self):
        handlers = self.BUILD_HANDLER_CONFIG
        handler_objs = []
        for handler in handlers:
            if isinstance(handler, basestring):
                handler_cls = importlib.resolve(handler)
                handler_obj = handler_cls()
            elif isinstance(handler, tuple):
                handler_name = handler[0]
                kwargs = handler[1]
                handler_cls = importlib.resolve(handler_name)
                handler_obj = handler_cls(**kwargs)
            elif isinstance(handler, BuildHandler):
                handler_obj = handler
            handler_objs.append(handler_obj)
        self.BUILD_HANDLERS = handler_objs
        return handler_objs

class UserSettingsHolder(BaseSettings):
    """
    Holder for user configured settings.
    """
    # SETTINGS_MODULE doesn't make much sense in the manually configured
    # (standalone) case.
    SETTINGS_MODULE = None

    def __init__(self, default_settings):
        """
        Requests for configuration variables not in this class are satisfied
        from the module specified in default_settings (if possible).
        """
        self.default_settings = default_settings

    def __getattr__(self, name):
        return getattr(self.default_settings, name)

    def __dir__(self):
        return self.__dict__.keys() + dir(self.default_settings)

    # For Python < 2.6:
    __members__ = property(lambda self: self.__dir__())

settings = LazySettings()

