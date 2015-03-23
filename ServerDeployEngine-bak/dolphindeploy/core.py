'''
Created on May 30, 2011

@author: chzhong
'''

import os

from dolphindeploy.parsers import PathConfigParser, OrderedDict
from dolphindeploy import settings

def normalize_role(role):
    '''
    Lookup the role name according to the alias name of the role.
    '''
    role = role.lower()
    if role in settings.ROLE_ALIAS:
        return settings.ROLE_ALIAS[role]
    return None

def normalize_roles(roles):
    '''
    Lookup the names of roles provided in the list 'roles'.
    Note:
        If an alias name is unavailable in the dict 'ROLE_ALIAS', 
        it would be discarded directly.
        This means that this function may accept a list containing 6
        items, but return a list containing only 4 items.
    '''
    if not isinstance(roles, (list, tuple, set)):
        return set([normalize_role(roles)])
    real_roles = []
    for role in roles:
        real_role = normalize_role(role)
        if real_role:
            real_roles.append(real_role)
    return set(real_roles)


def load_confset_config(confset):
    '''
    Loads environment configuration.
    
    The following path will be searched:
    conf/default/default.cfg
    conf/%(env)/%(env).cfg
    conf/%(env)/%(user_name).usr.cfg    
    
    While %(confset) is the environment name, %(user_name) is current login user.
    '''
    cp = PathConfigParser(dict_type=OrderedDict)
    paths = [
             'conf/default/default.cfg',
             'conf/%s/%s.cfg' % (confset, confset),
             'conf/%s/%s.usr.cfg' % (confset, os.getenv('LOGNAME'))
             ]
    print 'Loading configuration...'
    for path in paths:
        print path
    cp.read(paths)
    cp.defaults()['__confset__'] = confset
    return cp

def write_confset_config(confset, cp):
    '''
    Writes environment configuration to file.
    '''
    path = 'conf/%s/%s.cfg' % (confset, confset)
    with open(path, "w+") as fp:
        cp.write(fp)

def open_confset_config(confset):
    '''
    Open environment configuration.
    '''
    cp = PathConfigParser(dict_type=OrderedDict)
    paths = ['conf/%s/%s.cfg' % (confset, confset)]
    print 'Loading configuration for writing...'
    cp.read(paths)
    return cp

def open_confset_usr_config(confset):
    '''
    Open current user's environment configuration.
    '''
    cp = PathConfigParser(dict_type=OrderedDict)
    paths = ['conf/%s/%s.usr.cfg' % (confset, os.getenv('LOGNAME'))]
    print 'Loading user configuration for writing...'
    cp.read(paths)
    return cp



def write_confset_usr_config(confset, cp):
    '''
    Open current user's environment configuration to file.
    '''
    path = 'conf/%s/%s.usr.cfg' % (confset, os.getenv('LOGNAME'))
    with open(path, "w+") as fp:
        cp.write(fp)
