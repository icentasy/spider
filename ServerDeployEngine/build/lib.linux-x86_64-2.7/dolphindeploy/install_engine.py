'''
Created on Dec 12, 2011

@author: chzhong
'''
import os

from fabric.context_managers import cd
from fabric.operations import local, put, sudo, run
from fabric.state import env

from dolphindeploy import settings

def ensure_user(username):
    args = {
        'username' : username
    }
    run('[ -z `grep "^%(username)s:" /etc/passwd` ] && sudo useradd -r %(username)s -M -N' % args)

def ensure_remote_dirs(dirs):
    for d in dirs:
        sudo("mkdir -p -m a+rw %s" % d)

def install_packages(packages, verison, check_deps=False):
    '''
    Upload packages to remote server and install them.
    '''
    app_availble_dir = os.path.join(settings.APP_DIR, 'available')
    app_dist_dir = os.path.join(app_availble_dir, verison)
    app_enable_dir = os.path.join(settings.APP_DIR, 'enabled')
    app_log_dir = os.path.join(settings.APP_DIR, 'log')
    app_data_dir = os.path.join(settings.APP_DIR, 'data')
    ensure_remote_dirs([settings.APP_DIR, app_availble_dir, app_dist_dir, app_enable_dir, app_log_dir, app_data_dir])
    for app in packages:
        package = packages[app]
        package_name = os.path.basename(package)
        # if provide password ,use put instead of scp its no args for password
        if env.password:
            put(package, os.path.join(app_dist_dir, package_name), use_sudo=True)
        else:
            if env.port:
                env.host_string = env.host_string.replace(":%s" % env.port,"")
                local("scp -P %s -i %s  %s %s:%s" % (env.port, env.key_filename, package, env.host_string, os.path.join(app_dist_dir, package_name)))
                env.host_string = "%s:%s" % (env.host_string,env.port)
            else:
                local("scp -i %s %s %s:%s" % (env.key_filename, package, env.host_string, os.path.join(app_dist_dir, package_name)))

        with cd(app_dist_dir):
            sudo("tar xzf %s" % package_name)
            real_dir = os.path.join(app_dist_dir, package_name.replace('.tar.gz', ''))
            symb_dir = os.path.join(app_enable_dir, app)
            log_dir = os.path.join(app_log_dir, app)
            data_dir = os.path.join(app_data_dir, app)
            ensure_remote_dirs([log_dir, data_dir])
            sudo("rm -f %s" % symb_dir)
            sudo("ln -sf %s %s" % (real_dir, symb_dir))
        install_app(symb_dir, log_dir, data_dir, check_deps=check_deps)

def install_app(symb_dir, log_dir, data_dir, check_deps=False):
    with cd(symb_dir):
        sudo("chmod a+rw %s" % log_dir)
        sudo("chmod a+rw %s" % data_dir)
        sudo("chmod a+x scripts/*.sh")
        if check_deps:
            sudo("./%s checkdeps" % 'scripts/install.sh')
        else:
            sudo("./%s" % 'scripts/install.sh')
        sudo("./%s" % 'scripts/restart.sh')
