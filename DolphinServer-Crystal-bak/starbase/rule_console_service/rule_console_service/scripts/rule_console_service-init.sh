#!/bin/bash
#
# Dolphin Operation uWSGI Web Server init script
#
### BEGIN INIT INFO
# Provides:          dolphinop-service
# Required-Start:    $remote_fs $remote_fs $network $syslog
# Required-Stop:     $remote_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start Dolphin Operation Service uWSGI Web Server at boot time
# Description:       Dolphin Operation Service uWSGI Web Server provides web server backend.
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/var/app/enabled/rule_console
DAEMON=/usr/local/bin/uwsgi
NAME=RuleConsole
DESC="Rule Console Service uWSGI Web Server"
PROJECT=rule_console_service
SPIDERS=1
APP_DIR=/var/app/enabled/$PROJECT
PID_FILE=/var/run/$PROJECT-uwsgi.pid

if [ -f /etc/default/$PROJECT ]; then
	. /etc/default/$PROJECT
fi

function stop_uwsgi()
{
	if [ -f "${PID_FILE}" ]; then
	    export PID=`cat ${PID_FILE}`
	    rm "${PID_FILE}"
	    kill -INT ${PID} || echo "no such process ${PID}"
    else
        echo "${PROJECT} stop/waiting."
	fi
}

function start_uwsgi()
{
	if [ -f "$PID_FILE" ]; then
		echo "$NAME is already running."
	else
	    pushd ${APP_DIR}/rule_console >/dev/null
	    uwsgi --pidfile=${PID_FILE} --ini conf/uwsgi.cfg --uid dolphinop --gid nogroup
	    popd >/dev/null
	fi
}

set -e

. /lib/lsb/init-functions

case "$1" in
	start)
		echo "Starting $DESC..."
		start_uwsgi
		echo "Done."
		;;
	stop)
		echo "Stopping $DESC..."
		stop_uwsgi
		echo "Done."
		;;

	restart)
		echo "Restarting $DESC..."
		stop_uwsgi
        sleep 6
		start_uwsgi
		echo "Done."
		;;

	status)
		status_of_proc -p ${PID_FILE} "$DAEMON" uwsgi && exit 0 || exit $?
		;;
	*)
		echo "Usage: $NAME {start|stop|restart|status}" >&2
		exit 1
		;;
esac

exit 0

