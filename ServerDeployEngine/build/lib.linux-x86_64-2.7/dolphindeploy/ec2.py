'''
Created on May 30, 2011

@author: chzhong
'''
from dolphindeploy.core import load_confset_config, normalize_roles, normalize_role, \
    open_confset_config, write_confset_config, open_confset_usr_config, \
    write_confset_usr_config
import ConfigParser
import time

_confset = None

def _ensure_instance_id(cp, server):
    inst_id = cp.get(server, 'instance-id') if cp.has_option(server, 'instance-id') else None
    if not inst_id:
        inst_id = raw_input('Please enter the instance id for server %s: ' % server)
        if inst_id:
            cp.set(server, 'instance-id', inst_id)
    return inst_id

def _sync_server_ip(cp, server, instances_dict):
    inst_id = _ensure_instance_id(cp, server)
    if inst_id:
        instance = instances_dict[inst_id] if inst_id in instances_dict else None
        if instance and instance.state == 'running':
            ip = instance.private_ip_address
            dns = instance.public_dns_name
            print 'Updating server %s(%s): IP -> %s, DNS -> %s.' % (server, inst_id, ip, dns)
            cp.set(server, 'ip', ip)
            cp.set(server, 'dns', dns)
        else:
            print 'Instance %s not found or not running.' % inst_id
    else:
        print 'Skipped %s - instance id not specified.' % server

def _upgrade_server(cp, server, instance_type, instances_dict):
    global _confset
    inst_id = _ensure_instance_id(cp, server)
    if inst_id:
        instance = instances_dict[inst_id] if inst_id in instances_dict else None
        if not instance:
            print 'Instance %s not found.' % inst_id
            return
        if instance.instance_type == instance_type:
            return
        print 'Upgrading server %s(%s) from %s to %s.' % (server, inst_id, instance.instance_type, instance_type)
        if instance.state == 'running':
            print 'Stopping server...'
            instance.stop()
        while instance.state != 'stopped':
            time.sleep(1)
            instance.update()
        if instance.state == 'stopped':
            instance.modify_attribute('instanceType', type)
            print 'Starting server...'
            instance.start()
        while instance.state != 'running':
            time.sleep(1)
            instance.update()

        ip = instance.private_ip_address
        dns = instance.public_dns_name
        print 'Updating server %s(%s): IP -> %s, DNS -> %s.' % (server, inst_id, ip, dns)
        cp.set(server, 'ip', ip)
        cp.set(server, 'dns', dns)

        #config_server(_confset, server)
    else:
        print 'Skipped %s - instance id not specified.' % server


def _sync_role_ip(cp, role, instances_dict):
    real_role = normalize_role(role)
    servers = cp.sections()
    for server in servers:
        roles_repr = cp.get(server, 'roles')
        roles = normalize_roles(roles_repr.split(','))
        if real_role in roles:
            _sync_server_ip(cp, server, instances_dict)

def _upgrade_role(cp, role, instance_type, instances_dict):
    real_role = normalize_role(role)
    servers = cp.sections()
    for server in servers:
        roles_repr = cp.get(server, 'roles')
        roles = normalize_roles(roles_repr.split(','))
        if real_role in roles:
            _upgrade_server(cp, server, instance_type, instances_dict)


def _prepare_instances(conn):
    print 'Loading instance data from AWS...'
    reservations = conn.get_all_instances()
    instances_dict = {}
    for reservation in reservations:
        for instance in reservation.instances:
            instances_dict[instance.id] = instance
    return instances_dict

def _ensure_aws_access(confset, cp):
    aws_access_key_id = cp.get(ConfigParser.DEFAULTSECT, 'aws_access_key_id') if cp.has_option(ConfigParser.DEFAULTSECT, 'aws_access_key_id') else None
    aws_secret_access_key = cp.get(ConfigParser.DEFAULTSECT, 'aws_secret_access_key') if cp.has_option(ConfigParser.DEFAULTSECT, 'aws_secret_access_key') else None

    if not aws_access_key_id or not aws_secret_access_key:
        print '''You must provide your AWS Credentials in order to access your AWS.
You can get your AWS Credentials here: 
https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key

If the environment is not an AWS environment, press Ctrl+C to exit.'''
    while not aws_access_key_id:
        aws_access_key_id = raw_input('Please enter your AWS Access Key ID: ')
    while not aws_secret_access_key:
        aws_secret_access_key = raw_input('Please enter your AWS Secret Access Key: ')

    usr_cp = open_confset_usr_config(confset)
    usr_cp.set(ConfigParser.DEFAULTSECT, 'aws_access_key_id', aws_access_key_id)
    usr_cp.set(ConfigParser.DEFAULTSECT, 'aws_secret_access_key', aws_secret_access_key)
    write_confset_usr_config(confset, usr_cp)

    return aws_access_key_id, aws_secret_access_key

def ensure_ec2_connection(confset, cp):
    aws_access_key_id, aws_secret_access_key = _ensure_aws_access(confset, cp)
    from boto.ec2.connection import EC2Connection
    conn = EC2Connection(aws_access_key_id, aws_secret_access_key)
    return conn

def ensure_emr_connection(confset, cp):
    aws_access_key_id, aws_secret_access_key = _ensure_aws_access(confset, cp)
    from boto.emr.connection import EmrConnection
    conn = EmrConnection(aws_access_key_id, aws_secret_access_key)
    return conn

def sync_env_ip(confset, server=None, role=None):
    cp = load_confset_config(confset)
    conn = _ensure_aws_access(confset, cp)
    instances_dict = _prepare_instances(conn)

    cpw = open_confset_config(confset)
    if server:
        _sync_server_ip(cpw, server, instances_dict)
    elif role:
        _sync_role_ip(cpw, role, instances_dict)
    else:
        servers = cpw.sections()
        for server in servers:
            _sync_server_ip(cpw, server, instances_dict)

    write_confset_config(confset, cpw)

def upgrade_env(confset, instance_type, server=None, role=None):
    global _confset
    _confset = confset
    cp = load_confset_config(confset)
    conn = _ensure_aws_access(confset, cp)
    instances_dict = _prepare_instances(conn)

    cpw = open_confset_config(confset)
    if server:
        _upgrade_server(cpw, server, instance_type, instances_dict)
    elif role:
        _upgrade_role(cpw, role, instance_type, instances_dict)
    else:
        servers = cp.sections()
        for server in servers:
            _upgrade_server(cpw, server, instance_type, instances_dict)
    write_confset_config(confset, cpw)
    _confset = None
