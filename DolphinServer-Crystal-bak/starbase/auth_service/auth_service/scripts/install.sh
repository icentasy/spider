#!/bin/bash
#
# This scripts is used to install the application.
# This scripts is required for all projects.
#
#
# Author : kunli
#

python setup.py -q build

SCRIPT_DIR=`dirname $0`
PROJECT=auth_service

if [ "$1" = "checkdeps" ] ; then

    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
    fi
fi

if [ -f "${SCRIPT_DIR}/setup_conf.sh" ]; then
    ${SCRIPT_DIR}/setup_conf.sh
fi

python setup.py -q build

PTH_FILE='auth_service.pth'
if [ "$2" = "lib" ] ; then
    sudo python setup.py -q install
else
    pwd > ${PTH_FILE}
    sudo python scripts/install.py
fi

#echo Pre-compression the JS/CSS during deployment
#sudo python dolphinop/manage.py compress

echo Installing service...
test -z `grep "^dolphinop:" /etc/passwd`  && sudo useradd -r dolphinop -M -N

mkdir -p -m a+rw /var/app/data/$PROJECT/spool

chmod -R a+rw /var/app/data/$PROJECT/spool
chmod -R a+rw /var/app/log/$PROJECT
chown dolphinop:nogroup /var/app/data/$PROJECT/spool
chown dolphinop:nogroup /var/app/log/$PROJECT

ln -sf /var/app/enabled/$PROJECT/scripts/$PROJECT-init.sh /etc/init.d/$PROJECT
update-rc.d $PROJECT defaults

