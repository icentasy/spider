#!/usr/bin/python
# Copyright (c) 2011 Baina Info Inc. All rights reserved.
# author: chzong, kunli
# date:2011-04-11
import sys
import os
from optparse import OptionParser
print 'JUST TEST...'

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(HERE))

def deploy(options, args):
    from dolphindeploy import deploy_engine
    source = options.source
    env = options.destination
    args_len = len(args)
    if args_len >= 1:
        options.servers.append(args[0])
    if args_len >= 2:
        options.roles.append(args[1])
    deploy_engine.deploy(source, env, options.servers, options.roles, options.version, options.build_only, options.check_deps)

def sync_instance(options, args):
    from dolphindeploy import ec2
    env = options.destination
    args_len = len(args)
    server = args[0] if args_len >= 1 else None
    role = args[1] if args_len >= 2 else None
    ec2.sync_env_ip(env, server, role)

def upgrade_instance(options, args):
    from dolphindeploy import ec2
    env = options.destination
    args_len = len(args)
    instance_type = args[0] if args_len >= 1 else error('Missing instance type.')
    server = args[1] if args_len >= 2 else None
    role = args[2] if args_len >= 3 else None
    ec2.upgrade_env(env, instance_type, server, role)

def error(msg, exit_code=1):
    """Utility function for displaying fatal error messages with usage
    help.
    """
    sys.stderr.write(msg + "\n")
    sys.exit(exit_code)

def parse_args():
    """Deploy current source to a target destination environment.   
    %prog [deploy] destination [server [role]]
    %prog [deploy] destination [-r role]...
    %prog [deploy] destination [-s server]...

Sync IP, DNS information to configuration files from EC2.
    %prog sync_instance destination [server [role]]

Upgrade instance type on EC2.
    %prog upgrade_instance destination new_type [server [role]]
    
To see more, type "%prog --help".
"""
    parser = OptionParser(usage=parse_args.__doc__)
    parser.add_option('-S', '--settings',
                    action='store', type="string", dest='deploy_settings', default='conf/deploy_settings.py',
                    help='Specify path of the deploy settings script file. Defaults to "conf/deploy_settings.py".')
    parser.add_option('-B', '--build-only',
                    action='store_true', dest='build_only', default=False,
                    help='Build the deploy package only.')
    parser.add_option('-C', '--check-deps',
                    action='store_true', dest='check_deps', default=False,
                    help='Check and install dependencies if necessary when installing app.')
    parser.add_option('--source',
                    action='store', type="string", dest='source', default=".",
                    help='Specify the source code path to be deploy. Defaults to current directory.')
    parser.add_option('-s', '--server',
                    action='append', dest='servers', default=[],
                    help='Specify the server to deploy to. If ignored, all servers will be deployed.  You can specify multiple servers at one time.')
    parser.add_option('-r', '--role',
                    action='append', dest='roles', default=[],
                    help='Specify the role to deploy. If ignored, all roles will be deployed. You can specify multiple roles at one time.')
    parser.add_option('-v', '--version',
                    action='store', type="string", dest='version', default=None,
                    help='Specify the version label of the source code or deploy. Defaults to SVN revision number or Git\'s commit id')
    options, args = parser.parse_args()

    import dolphindeploy
    dolphindeploy.SETTINGS_MODULE_PATH = options.deploy_settings

    def syntax_error(msg):
        """Utility function for displaying fatal error messages with usage help."""
        sys.stderr.write("Syntax error: " + msg + "\n")
        sys.stderr.write(parser.get_usage())
        sys.exit(1)

    arg_len = len(args)
    if arg_len < 1:
        syntax_error('Invalid number of arguments.')

    first_arg = args[0]
    if first_arg not in __all__:
        options.command = "deploy"
        options.destination = first_arg
        args = args[1:]
    elif arg_len < 2:
        syntax_error('Invalid number of arguments.')
    else:
        options.command = first_arg
        options.destination = args[1]
        args = args[2:]

    if not options.command in __all__:
        syntax_error('Unsupported command "%s".' % options.command)

    return options, args

def main():
    options, args = parse_args()
    command = options.command
    func = globals()[command]
    func(options, args)

__all__ = [
    'deploy',
    'sync_instance',
    'upgrade_instance',
]

if '__main__' == __name__:
    main()
