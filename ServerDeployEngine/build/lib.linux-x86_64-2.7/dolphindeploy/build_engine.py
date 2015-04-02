'''
Created on Dec 12, 2011

@author: chzhong
'''

import os
import re
from ConfigParser import MAX_INTERPOLATION_DEPTH

from fabric.context_managers import lcd, settings as fab_settings
from fabric.operations import local
from fabric.utils import abort, warn

from dolphindeploy import settings
from dolphindeploy.parsers import OrderedDict, CombinedConfigParser

svc = settings.VERSION_CONTROL_MODULE

_KEYCRE = re.compile(r"%\(([^)]*)\)s|.")
_TEMPLTERE = re.compile(r"###template(?P<group>\([a-z_0-9]+\))?(?P<template>.*?)###", re.DOTALL | re.IGNORECASE)

def build_role(source, cp, server, role_or_roles):
    print '++++++++', source, cp, server, role_or_roles
    project_dir = prepare_source(source)
    role_apps = OrderedDict()
    if not isinstance(role_or_roles, (list, set)):
        role_or_roles = [role_or_roles]
    if isinstance(role_or_roles, (list, set)):
        for role in role_or_roles:
            apps = settings.ROLE_APPS_TABLE.get(role, ())
            for app in apps:
                role_apps[app] = True
    confset = cp.defaults()['__confset__']
    conf_dir = os.path.join(settings.CONF_ROOT, confset)
    packages = OrderedDict()
    for app in role_apps:
        package = build_app_package(cp, server, project_dir, app, conf_dir)
        packages[app] = package
    return packages


def handle_configuration(cp, server, app_dir, app_conf_template_dir, def_conf_template_dir):
    confs = find_confs(app_dir)
    for conf in confs:
        basepath = os.path.relpath(conf, app_dir)
        app_conf_base = os.path.join(app_conf_template_dir, basepath)
        def_conf_base = os.path.join(def_conf_template_dir, basepath)
        app_conf_template = app_conf_base + ".in"
        def_conf_template = def_conf_base + ".in"
        if os.path.exists(app_conf_template):
            print 'Generate: %s -> "%s"' % (basepath + ".in", basepath)
            _generate_conf(app_conf_template, conf, cp, server)
        elif os.path.exists(def_conf_template):
            print 'Generate: default/%s -> "%s"' % (basepath + ".in", basepath)
            _generate_conf(def_conf_template, conf, cp, server)
        elif os.path.exists(app_conf_base):
            print 'Copy: %s -> "%s"' % (basepath, basepath)
            local("cp -f %s %s" % (app_conf_base, conf))
        elif os.path.exists(def_conf_base):
            print 'Copy: default/%s -> "%s"' % (basepath, basepath)
            local("cp -f %s %s" % (def_conf_base, conf))
        else:
            print 'Not changed: %s' % basepath

def build_app_package(cp, server, project_dir, app, conf_dir):
    app_dir = os.path.join(project_dir, app)
    #app_conf_template_dir = os.path.join(conf_dir, app)
    #def_conf_template_dir = os.path.join(settings.DEFAULT_CONF_DIR, app)
    with fab_settings(warn_only=True, echo_stdin=False):
        if os.path.exists(app_dir):
            handlers = settings.ensure_build_handlers()
            for handler in handlers:
                handler(config_parser=cp, server=server, project_dir=project_dir, app_name=app)
            #handle_configuration(cp, server, app_dir, app_conf_template_dir, def_conf_template_dir)
            return _generate_package(app_dir)
        else:
            abort('app dir %s  does not exist' % app_dir)

def _generate_package(app_dir):
    with lcd(app_dir):
        with fab_settings(warn_only=True):
            if not os.path.exists(os.path.join(app_dir, 'setup.py')):
                abort('setup.py is not in %s ' % app_dir)
            build_script_dir = os.path.join(app_dir, 'scripts/build.sh')
            if os.path.exists(build_script_dir) and os.access(build_script_dir, os.X_OK):
                local(build_script_dir)
            else:
                local("python setup.py -q sdist")
            app_dist_dir = os.path.join(app_dir, 'dist')
            filepath = os.listdir(app_dist_dir)[0]
            local("mv -f dist/*.tar.gz %s/" % settings.DIST_TEMP)
            filepath = os.path.join(settings.DIST_TEMP, filepath)
            return filepath

def _generate_generic(template, output, base_cp, server):
    with open(template, "r") as fin:
        content = fin.read()
        global _cp
        _cp = base_cp
        content = _TEMPLTERE.sub(_interpolate_template, content)
        _cp = None
        args = base_cp.extravars(server)
        args.update(base_cp.defaults())
        content = _interpolate(content, args)
        with open(output, "w+") as fout:
            fout.write(content)

def _generate_cfg(template, output, base_cp, server):
    template_cp = CombinedConfigParser()
    template_cp.read([template])
    template_cp.set_base(base_cp)
    with open(output, "w+") as fp:
        template_cp.dump(server, fp)

CONF_GENERATOR = {
    '.conf' : _generate_cfg,
    '.cfg' : _generate_cfg
}

def _generate_conf(template, output, base_cp, server):
    _, ext = os.path.splitext(output)
    if ext in CONF_GENERATOR:
        generator = CONF_GENERATOR[ext]
    else:
        generator = _generate_generic
    generator(template, output, base_cp, server)

def _interpolate_template(match):
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
        sub = _interpolate(template, args)
        subs.append(sub)
    return "\r\n".join(subs)

def _interpolation_replace(match):
        s = match.group(1)
        if s is None:
            return match.group()
        else:
            return "%%(%s)s" % s.lower()

def _interpolate(rawval, args):
    value = rawval
    depth = MAX_INTERPOLATION_DEPTH
    while depth:                    # Loop through this until it's done
        depth -= 1
        if "%(" in value:
            value = _KEYCRE.sub(_interpolation_replace, value)
            try:
                value = value % args
            except KeyError, e:
                warn('Key not found : %s' % e)
        else:
            break
    return value

def is_conf_file(filename):
    basename = os.path.basename(filename)
    if basename.lower() in settings.CONF_NAME_PATTERN:
        return True
    ext = os.path.splitext(filename)[1]
    if ext.lower() in settings.CONF_EXT_PATTERN:
        return True
    return False

def find_confs(root):
    confs = []
    for r, _, files in os.walk(root):
        conf_files = filter(is_conf_file, files)
        conf_files = map(lambda p: os.path.join(r, p), conf_files)
        confs += conf_files
    return sorted(confs)

def prepare_source(source):
    get_source_cmd = None
    if svc.check_path(source):
        get_source_cmd = svc.get_prepare_command(source, settings.PROJECT_NAME)
    elif os.path.isdir(source):
        get_source_cmd = "cp -rf -L %s %s" % (source, settings.PROJECT_NAME)
    else:
        raise ValueError('The given source "%s" is unrecognizable.')
    project_dir = os.path.join(settings.BUILD_TEMP, settings.PROJECT_NAME)
    with fab_settings(warn_only=True):
        if not os.path.exists(settings.TEMP_DIR):
            local("mkdir %s" % settings.TEMP_DIR)
        if not os.path.exists(settings.BUILD_TEMP):
            local("mkdir %s" % settings.BUILD_TEMP)
        if os.path.exists(project_dir):
            local("rm -rf %s" % project_dir)
        with lcd(settings.BUILD_TEMP):
            local(get_source_cmd)
        if not os.path.exists(settings.DIST_TEMP):
            local("mkdir %s" % settings.DIST_TEMP)
        else:
            local("rm -rf %s/*" % settings.DIST_TEMP)

    return project_dir

