'''
Created on Dec 23, 2011

@author: chzhong
'''
import os
import re
import sys
import tempfile

from fabric.operations import local
from fabric.utils import warn

from dolphindeploy.parsers import CombinedConfigParser
from dolphindeploy import settings, BuildHandler

class FileBuildHandler(BuildHandler):
    '''A handler that handle files in before building packages.
    '''

    def find_files(self, **kwargs):
        raise NotImplemented()

    def handle_file(self, path, **kwargs):
        raise NotImplemented()

    def handle(self, **kwargs):
        files = self.find_files(**kwargs)
        for file_path in files:
            self.handle_file(path=file_path, **kwargs)

class ConfigurationFileHandler(FileBuildHandler):
    """Handler that generate configuration files from configuration template or file.
    
    Replace Rules:
        1. Try to generate the file from conf/ENV/APP/CONF_NAME.in (if exists).
        2. Try to generate the file from conf/default/APP/CONF_NAME.in (if exists).
        3. Try to use the file from conf/ENV/APP/CONF_NAME (if exists).
        4. Try to use the file from conf/default/APP/CONF_NAME (if exists).
        5. Use the file from APP/CONF_NAME.
    while ENV is the destination to be deploy, APP is the application name, CONF_NAME is the name of configuration file.    
    
    settings:
        CONF_NAME_PATTERN, EXTRA_CONF_NAME_PATTERN:
            Configuration file name patterns. 
            Files which has a name defined in these tuples will be consider as configuration files.
            Default values:(
                'settings2.py',
                'version',
                'files',
                'passwd',
                's3cfg'
            )
        CONF_EXT_PATTERN, CONF_EXT_PATTERN:
            Configuration file extension patterns.
            Files with an extension defined in these tuples will be consider as configuration files.
            Default values:(
                '.conf',
                '.cfg',
                '.xml',
                '.csv',
                '.crt',
                '.key',
                '.pem',
                '.pub',
                '.nginx',
                '.logrotate',
                '.cron',
            )
            
    """

    def find_files(self, app_dir, **kwargs):
        confs = []
        for r, _, files in os.walk(app_dir):
            conf_files = filter(ConfigurationFileHandler.is_conf_file, files)
            conf_files = map(lambda p: os.path.join(r, p), conf_files)
            confs += conf_files
        return sorted(confs)

    def handle_file(self, path, config_parser, server, app_dir, def_conf_template_dir, app_conf_template_dir, **kwargs):
        basepath = os.path.relpath(path, app_dir)
        app_conf_base = os.path.join(app_conf_template_dir, basepath)
        def_conf_base = os.path.join(def_conf_template_dir, basepath)
        app_conf_template = app_conf_base + ".in"
        def_conf_template = def_conf_base + ".in"
        if os.path.exists(app_conf_template):
            print 'Generate: %s -> "%s"' % (basepath + ".in", basepath)
            self._generate_conf(app_conf_template, path, config_parser, server)
        elif os.path.exists(def_conf_template):
            print 'Generate: default/%s -> "%s"' % (basepath + ".in", basepath)
            self._generate_conf(def_conf_template, path, config_parser, server)
        elif os.path.exists(app_conf_base):
            print 'Copy: %s -> "%s"' % (basepath, basepath)
            local("cp -f %s %s" % (app_conf_base, path))
        elif os.path.exists(def_conf_base):
            print 'Copy: default/%s -> "%s"' % (basepath, basepath)
            local("cp -f %s %s" % (def_conf_base, path))
        else:
            print 'Not changed: %s' % basepath

    def handle(self, config_parser, server, project_dir, app_name, **kwargs):
        confset = config_parser.defaults()['__confset__']
        conf_dir = os.path.join(settings.CONF_ROOT, confset)
        app_dir = os.path.join(project_dir, app_name)
        app_conf_template_dir = os.path.join(conf_dir, app_name)
        def_conf_template_dir = os.path.join(settings.DEFAULT_CONF_DIR, app_name)
        FileBuildHandler.handle(self, config_parser=config_parser,
                                server=server,
                                project_dir=project_dir,
                                app_name=app_name,
                                app_dir=app_dir,
                                app_conf_template_dir=app_conf_template_dir,
                                def_conf_template_dir=def_conf_template_dir,
                                 **kwargs)

    def _generate_generic(self, template, output, base_cp, server):
        with open(template, "r") as fin:
            content = fin.read()
            global _cp
            _cp = base_cp
            content = self._TEMPLTERE.sub(self._interpolate_template, content)
            _cp = None
            args = base_cp.extravars(server)
            args.update(base_cp.defaults())
            content = ConfigurationFileHandler._interpolate(content, args)
            with open(output, "w+") as fout:
                fout.write(content)

    def _generate_cfg(self, template, output, base_cp, server):
        if sys.version_info < (2,7):
            template_cp = CombinedConfigParser()
        else:
            template_cp = CombinedConfigParser(allow_no_value=True)
        template_cp.read([template])
        template_cp.set_base(base_cp)
        with open(output, "w+") as fp:
            template_cp.dump(server, fp)

    CONF_GENERATOR = {
        '.conf' : '_generate_cfg',
        '.cfg' : '_generate_cfg'
    }

    _KEYCRE = re.compile(r"%\(([^)]*)\)s|.")
    _TEMPLTERE = re.compile(r"###template(?P<group>\([a-z_0-9]+\))?(?P<template>.*?)###", re.DOTALL | re.IGNORECASE)

    def _generate_conf(self, template, output, base_cp, server):
        _, ext = os.path.splitext(output)
        if ext in ConfigurationFileHandler.CONF_GENERATOR:
            generator = getattr(self, ConfigurationFileHandler.CONF_GENERATOR[ext])
        else:
            generator = self._generate_generic
        generator(template, output, base_cp, server)

    def _interpolate_template(self, match):
        global _cp
        cp = _cp
        sections = cp.sections()
        if match.group("group"):
            group = match.group("group").strip('()')
            sections = filter(lambda s: cp.get(s, 'group') == group, sections)
        template = match.group("template")
        subs = []
        for section in sections:
            args = cp.extravars(section)
            args.update(cp.defaults())
            sub = ConfigurationFileHandler._interpolate(template, args)
            sub = sub.strip('\r')
            sub = sub.strip('\n')
            subs.append(sub)
        return "\r\n".join(subs)

    @staticmethod
    def _interpolation_replace(match):
            s = match.group(1)
            if s is None:
                return match.group()
            else:
                return "%%(%s)s" % s.lower()

    @staticmethod
    def _interpolate(rawval, args):
        from ConfigParser import MAX_INTERPOLATION_DEPTH
        value = rawval
        depth = MAX_INTERPOLATION_DEPTH
        while depth:                    # Loop through this until it's done
            depth -= 1
            if "%(" in value:
                value = ConfigurationFileHandler._KEYCRE.sub(ConfigurationFileHandler._interpolation_replace, value)
                try:
                    value = value % args
                except KeyError, e:
                    warn('Key not found : %s' % e)
            else:
                break
        return value

    @staticmethod
    def is_conf_file(filename):
        basename = os.path.basename(filename)
        if basename.lower() in settings.CONF_NAME_PATTERN:
            return True
        ext = os.path.splitext(filename)[1]
        if ext.lower() in settings.CONF_EXT_PATTERN:
            return True
        return False

class CompressResourceHandler(FileBuildHandler):
    """Handler to compress resource files.
    
    arguments:
        'engine':  The path to, or command line to run, the resource compress engine.
        'args':    The command arguments to pass to the engine. 
                   Use the following place-holders for file paths:
                   %(path)s    The path to the input resource file.
                   %(root)s    The main file name of the resource file.
                   %(ext)s     The extension of the resource file (without a heading '.').
                   %(output_path)s
                               The path to the output file. 
                               We output this to a temp file and copy it back.  
                               
    data:
        'RESOURCE_EXT_PATTERN'
                    A tuple of resource file extensions pattern to search.
                    Each extension should have a heading '.'.
    """
    RESOURCE_EXT_PATTERN = ()
    RESOURCE_EXCLUDE_PATTERN = (".min",)

    def is_resource_file(self, filename):
        _, ext = os.path.splitext(filename)
        for exclude_pattern in self.RESOURCE_EXCLUDE_PATTERN:
            if exclude_pattern in filename:
                return False
        if ext.lower() in self.RESOURCE_EXT_PATTERN:
            return True
        return False

    def __init__(self, engine, args=(), **kwargs):
        if 'excludes' not in kwargs:
            kwargs['excludes'] = ('default', "dev", 'local')
        FileBuildHandler.__init__(self, **kwargs)
        self.engine = engine
        self.args = args

    def find_files(self, app_dir, **kwargs):
        confs = []
        for r, _, files in os.walk(app_dir):
            conf_files = filter(self.is_resource_file, files)
            conf_files = map(lambda p: os.path.join(r, p), conf_files)
            confs += conf_files
        return sorted(confs)

    def handle_file(self, path, **kwargs):
        print 'Compressing resource "%s"...' % path
        raw_cmdline = "%s %s" % (self.engine, " ".join(self.args))
        _, temp_path = tempfile.mkstemp()
        root, ext = os.path.splitext(os.path.basename(path))
        cmdline = raw_cmdline % { 'path' : path, 'output_path' : temp_path, 'ext' : ext[1:], 'root' : root }
        local(cmdline)
        with open(path, 'w') as out_fp:
            with open(temp_path, 'r') as in_fp:
                out_fp.write(in_fp.read())
        os.remove(temp_path)

    def handle(self, config_parser, server, project_dir, app_name, **kwargs):
        print 'Compressing resources (Engine: %s, Pattern: %s)...' % (self.engine, self.RESOURCE_EXT_PATTERN)
        app_dir = os.path.join(project_dir, app_name)
        FileBuildHandler.handle(self, config_parser=config_parser,
                                server=server,
                                project_dir=project_dir,
                                app_name=app_name,
                                app_dir=app_dir,
                                 **kwargs)
        print 'Compressed all resources (Engine: %s, Pattern: %s)...' % (self.engine, self.RESOURCE_EXT_PATTERN)

class GoogleClosureJavaScriptCompiler(CompressResourceHandler):
    """Google Closure Compiler
    
    settings:
        GC_LIB_PATH    The path to the Google Closure Compiler jar file (compiler.jar).
    
    A library to compress js files provided by Google.
    
    See more at http://code.google.com/closure/compiler/.
    """

    RESOURCE_EXT_PATTERN = (".js",)

    def __init__(self, **kwargs):
        CompressResourceHandler.__init__(self, 'java -jar "%s"' % settings.GC_LIB_PATH, args=('--js "%(path)s"', '--js_output_file "%(output_path)s"'), **kwargs)

class YUIResourceCompressor(CompressResourceHandler):
    """YUI Compressor
    
    settings:
        YUI_LIB_PATH    The path to the YUI Compressor jar file (yuicompressor-x.y.z.jar).
    
    A library to compress js files and css files provided by Yahoo.
    See more at http://developer.yahoo.com/yui/compressor/.
    """

    RESOURCE_EXT_PATTERN = (".js", ".css")

    def __init__(self, **kwargs):
        CompressResourceHandler.__init__(self, 'java -jar "%s"' % settings.YUI_LIB_PATH, args=('--type %(ext)s', '"%(path)s"', '-o "%(output_path)s"'), **kwargs)

class YUIJavaScriptCompressor(CompressResourceHandler):
    """YUI Compressor's JavaScript Minifier
    
    settings:
        YUI_LIB_PATH    The path to the YUI Compressor jar file (yuicompressor-x.y.z.jar).
    
    A library to compress js files provided by Yahoo.
    See more at http://developer.yahoo.com/yui/compressor/.
    """

    RESOURCE_EXT_PATTERN = (".js",)

    def __init__(self, **kwargs):
        CompressResourceHandler.__init__(self, 'java -jar "%s"' % settings.YUI_LIB_PATH, args=('--type js', '"%(path)s"', '-o "%(output_path)s"'), **kwargs)


class YUICSSCompressor(CompressResourceHandler):
    """YUI Compressor's CSS minifier
    
    settings:
        YUI_LIB_PATH    The path to the YUI Compressor jar file (yuicompressor-x.y.z.jar).
    
    A library to compress css files provided by Yahoo.
    See more at http://developer.yahoo.com/yui/compressor/css.html.
    """
    RESOURCE_EXT_PATTERN = (".css",)

    def __init__(self, **kwargs):
        CompressResourceHandler.__init__(self, 'java -jar "%s"' % settings.YUI_LIB_PATH, args=('--type css', '"%(path)s"', '-o "%(output_path)s"'), **kwargs)
