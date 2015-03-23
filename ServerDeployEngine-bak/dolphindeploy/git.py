'''
Created on Apr 19, 2011

@author: chzhong
'''
from fabric.operations import local
from threading import Event

def query_revision(path, callback):
    commit_log = local('git log -n 1 "%s"' % path, capture=True)
    commit_lines = commit_log.splitlines()
    commit_info = commit_lines[0]
    object_id = commit_info[commit_info.find(' ') + 1:]
    callback(object_id)

def build_version(revision):
    return 'git%s' % revision[:7]

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
    return 'git clone "%s" "%s"' % (path, dest)

def check_path(path):
    '''
    Determine whether a path is an SVN path.
    '''
    return False
"""
    o = urlparse(path)
    try:
        return 'git' == o.scheme.lower()
    except AttributeError:
        return False
"""
