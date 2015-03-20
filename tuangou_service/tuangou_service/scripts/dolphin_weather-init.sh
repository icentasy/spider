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

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/var/app/enabled/tuangou_service
DAEMON=/usr/local/bin/uwsgi
NAME=TuanGou
DESC="TuanGou Service uWSGI Web Server"
PROJECT=tuangou_service
SPIDERS=1
APP_DIR=/var/app/enabled/$PROJECT
PID_FILE=/var/run/$PROJECT-uwsgi.pid
CELERY_LOG_FILE=/var/app/log/tuangou_service/worker.log
BEAT_PID_FILE=/var/app/log/tuangou_service/beat.pid
BEAT_LOG_FILE=/var/app/log/tuangou_service/beat.log

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
	    pushd ${APP_DIR}/dolphin_weather >/dev/null
	    uwsgi --pidfile=${PID_FILE} --ini conf/uwsgi.cfg --uid dolphinop --gid nogroup
	    popd >/dev/null
	fi
}


stop_beat()
{
    echo "stop beat..."
	if [ -f "${BEAT_PID_FILE}" ]; then
	    export BEAT_PID=`cat ${BEAT_PID_FILE}`
	    rm "${BEAT_PID_FILE}"
	    kill -INT ${BEAT_PID} || echo "no such process ${PID}"
    else
        echo "celerybeat stop/waiting."
	fi
}

start_beat()
{
    echo "start beat..."
	if [ -f "$BEAT_PID_FILE" ]; then
		echo "celerybeat is already running."
	else
        nohup celery beat --workdir=${APP_DIR}/dolphin_weather \
          --app=crawler.celeryapp:app \
          --pidfile=$BEAT_PID_FILE \
          --loglevel=info \
          --logfile=$BEAT_LOG_FILE > /dev/null 2>&1 &
    fi
}

stop_worker()
{
    echo "stoping celery worker..."
    if pgrep -f $CELERY_LOG_FILE > /dev/null 2>&1;then
        pkill -9 -f $CELERY_LOG_FILE
    fi
}

start_worker()
{
    if pgrep -f $CELERY_LOG_FILE > /dev/null 2>&1; then
        echo "celery worker is already running"
    else
        echo "starting celery worker..."
        celery multi start 6 -Q:1 hot_city -Q:2 alert_weather \
          -Q:3-6 common_city_alert_weather \
          --app=crawler.celeryapp:app \
          --loglevel=info \
          --workdir=${APP_DIR}/dolphin_weather \
          --logfile=$CELERY_LOG_FILE
    fi
}

set -e

. /lib/lsb/init-functions

case "$1" in
	start)
		echo "Starting $DESC..."
        start_worker
        start_beat
		start_uwsgi
		echo "Done."
		;;
	stop)
		echo "Stopping $DESC..."
		stop_uwsgi
        stop_beat
        stop_worker
		echo "Done."
		;;

	restart)
		echo "Restarting $DESC..."
		stop_uwsgi
        stop_beat
        stop_worker
        sleep 6
        start_worker
        start_beat
		start_uwsgi
		echo "Done."
		;;

    start-celery)
        echo "Starting $NAME celery..."
        start_worker
        start_beat
        echo "Done."
        ;;

    stop-celery)
        echo "Stoping $NAME celery..."
        stop_beat
        stop_worker
        echo "Done."
        ;;

    restart-celery)
        echo "Restarting $NAME celery..."
        stop_beat
        stop_worker
        sleep 6
        start_worker
        start_beat
        echo "Done."
        ;;

    stop-beat)
        echo "Stoping $NAME beat..."
        stop_beat
        echo "Done."
        ;;

    start-beat)
        echo "Starting $NAME beat..."
        start_beat
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

