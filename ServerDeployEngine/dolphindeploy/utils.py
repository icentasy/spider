'''
Created on Dec 12, 2011
@author: chzhong
'''

from fabric.state import env
from fabric.network import join_host_strings


def setup_host(cp, server):
    '''
    Setup host configuration for fabric.
    Will connect using a server's dns (public address) using configured user:port pair.
    If a keyfile is specified, the keyfile will be used to connect to the server;
    otherwise password will be used if configured.
    '''

    host = cp.get(server, 'dns')
    user = cp.get(server, 'user') if cp.has_option(server, 'user') else None
    port = cp.getint(server, 'port') if cp.has_option(server, 'port') else None
    gateway = cp.get(server, 'gateway') if cp.has_option(server, 'gateway') else None
    host_string = join_host_strings(user, host, port) if user or port else host
    env.port = port
    env.host_string = host_string

    password = cp.get(server, 'password') if cp.has_option(
        server, 'password') else None

    keyfile = cp.get(server, 'keyfile') if cp.has_option(
        server, 'keyfile') else None

    if password:
        env.password = password
        env.passwords[host_string] = password

    if keyfile:
        env.key_filename = keyfile

    if gateway:
        env.gateway = gateway
