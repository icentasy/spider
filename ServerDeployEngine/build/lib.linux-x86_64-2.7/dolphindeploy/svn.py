'''
Created on Apr 19, 2011

@author: chzhong
'''
from fabric.operations import local
from threading import Event
from urlparse import urlparse
import xml.parsers.expat

def query_revision(path, callback):
    info_xml = local('svn info "%s" --xml' % path, capture=True)
    def entry_handler(name, attrs):
        if 'entry' == name and 'revision' in attrs:
            revision = int(attrs['revision'])
            callback(revision)
    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = entry_handler
    parser.Parse(info_xml, True)


def build_version(revision):
    return 'r%d' % revision

__rev = None

def get_version(path):
    event = Event()
    event.clear()
    def revision_handler(revision):
        global __rev
        __rev = revision
        event.set()
    query_revision(path, revision_handler)
    event.wait()
    global __rev
    version = build_version(__rev)
    return version

def get_prepare_command(path, dest):
    return 'svn export --force "%s" "%s"' % (path, dest)

def check_path(path):
    '''
    Determine whether a path is an SVN path.
    '''
    o = urlparse(path)
    try:
        return 'svn' == o.scheme.lower() and len(o.netloc) > 0
    except AttributeError:
        return False
