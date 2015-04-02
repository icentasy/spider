'''
# Taken from Python 2.7 with permission from/by the original author.

Created on Dec 12, 2011

@author: chzhong
'''
import sys
import os


# We might want to use a different one, e.g. importlib
importer = __import__

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for _ in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    importer(name)
    return sys.modules[name]

def import_file(path):
    """Import a Python script as a module.
    """
    if not os.path.exists(path):
        return
    dirname = os.path.dirname(os.path.abspath(path))
    if dirname not in sys.path:
        sys.path.append(dirname)
    basename = os.path.basename(path)
    name, _ = os.path.splitext(basename)
    importer(name)
    return sys.modules[name]



def resolve(s):
    """
    Resolve strings to objects using standard import and attribute
    syntax.
    """
    name = s.split('.')
    used = name.pop(0)
    try:
        found = importer(used)
        for frag in name:
            used += '.' + frag
            try:
                found = getattr(found, frag)
            except AttributeError:
                importer(used)
                found = getattr(found, frag)
        return found
    except ImportError:
        e, tb = sys.exc_info()[1:]
        v = ValueError('Cannot resolve %r: %s' % (s, e))
        v.__cause__, v.__traceback__ = e, tb
        raise v
