#!/bin/bash
#
# This scripts is used to install the application.
# This scripts is required for all projects.
#
#
# Author : kunli
#
echo "start install.sh"
python setup.py -q build

SCRIPT_DIR=`dirname $0`
PROJECT=Broodling

if [ "$1" = "checkdeps" ] ; then

    if [ -f "${SCRIPT_DIR}/install_deps.sh" ]; then
        ${SCRIPT_DIR}/install_deps.sh
    fi
fi

if [ -f "${SCRIPT_DIR}/setup_conf.sh" ]; then
    ${SCRIPT_DIR}/setup_conf.sh
fi

python setup.py -q build

PTH_FILE='Broodling.pth'
if [ "$2" = "lib" ] ; then
    sudo python setup.py -q install
else
    pwd > ${PTH_FILE}
    sudo python scripts/install.py
fi

ln -sf /srv/www/$PROJECT/scripts/$PROJECT-init.sh /etc/init.d/$PROJECT
update-rc.d $PROJECT defaults
