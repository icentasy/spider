'''
Created on Apr 19, 2011

@author: chzhong, kunli, congliu

'''
import os


from dolphindeploy import settings
from dolphindeploy.utils import setup_host
from dolphindeploy.core import normalize_roles, load_confset_config
from dolphindeploy.build_engine import build_role
from dolphindeploy.install_engine import install_packages

svc = settings.VERSION_CONTROL_MODULE

#CHECK_DEPENDENCIES = False
_cp = None

def deploy(source, confset, servers=None, roles=None, version=None, build_only=False, check_deps=False):
    if servers and roles:
        deploy_role(source, confset, servers, roles, version=version, build_only=build_only, check_deps=check_deps)
    elif servers:
        deploy_servers(source, confset, servers, version=version, build_only=build_only, check_deps=check_deps)
    elif roles:
        deploy_role(source, confset, None, roles, version=version, build_only=build_only, check_deps=check_deps)
    else:
        deploy_confset(source, confset, version=version, build_only=build_only, check_deps=check_deps)


def perpare_args(source, confset, version=None, roles=None):
    cp = load_confset_config(confset)
    if not svc.check_path(source) and os.path.isdir(source):
        source = os.path.abspath(source)
    if not version:
        version = svc.get_version(source)
    if roles:
        roles = normalize_roles(roles)
    return cp, source, version, roles

def deploy_confset(source, confset, version=None, build_only=False, check_deps=False):
    '''
    Deploys all roles to all servers.
    '''
    cp, source, version, _ = perpare_args(source, confset, version=version)
    print "Deploying %s to %s..." % (source, confset)
    servers = cp.sections()
    for server in servers:
        _deploy_server(source, cp, server, version, build_only=build_only, check_deps=check_deps)

def deploy_servers(source, confset, servers, version=None, build_only=False, check_deps=False):
    '''
    Deploy all roles in one server
    '''
    cp, source, version, _ = perpare_args(source, confset, version=version)
    print "Deploying %s to servers:%s..." % (source, ','.join(servers))
    for server in servers:
        print 'Deploying server "%s" (Source = %s, confset = %s)...' % (server, source, confset)
        _deploy_server(source, cp, server, version, build_only=build_only, check_deps=check_deps)

def _deploy_server(source, cp, server, version=None, build_only=False, check_deps=False):
    '''
    Detail deploy actions to a single server.
    '''
    setup_host(cp, server)
    roles_repr = cp.get(server, 'roles')
    print 'Server : %s, Source : %s, Roles : %s' % (server, source, roles_repr)
    roles = normalize_roles(roles_repr.split(','))
    _deploy_role(source, cp, server, roles, version, build_only=build_only, check_deps=check_deps)

def deploy_role(source, confset, servers, roles, version=None, build_only=False, check_deps=False):
    '''
    Deploy a single role to a single role.
    '''
    cp, source, version, roles = perpare_args(source, confset, version=version, roles=roles)
    if not servers:
        servers = cp.sections()
    for server in servers:
        roles_repr = cp.get(server, 'roles')
        server_roles = normalize_roles(roles_repr.split(','))
        target_roles = server_roles & roles if roles else server_roles
        if not target_roles:
            continue
        setup_host(cp, server)
        print 'Deploying roles:%s to server:%s...' % (",".join(target_roles), server)
        _deploy_role(source, cp, server, target_roles, version, build_only=False, check_deps=check_deps)

def _deploy_role(source, cp, server, role_or_roles, version=None, build_only=False, check_deps=False):
    cp.defaults()['webzine_version'] = version
    packages = build_role(source, cp, server, role_or_roles)
    if build_only:
        return
    install_packages(packages, version, check_deps=check_deps)
