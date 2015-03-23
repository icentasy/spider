#!/bin/bash
#
# Broodling init script
# 
### BEGIN INIT INFO
# Provides:          Broodling 
# Required-Start:    $remote_fs $remote_fs $network $syslog
# Required-Stop:     $remote_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

NAME=Broodling
DESC="Broodling for DolphinService statistics"
PROJECT=Broodling
SPIDERS=1
APP_DIR=/srv/www/$PROJECT/dolphin_stat.py
ERR_DIR=/srv/www/$PROJECT/log/error.log

function stop_stat()
{
    PID=`ps ax | grep /srv/www/Broodling/dolphin_stat | grep -v grep | awk {'print $1'} | awk {'print $1'}`
	if [ $PID ]; then
	    kill -TERM ${PID}
    else
        echo "${PROJECT} stop/waiting."
	fi
}

function start_stat()
{
	if [ `ps ax|grep /srv/www/Broodling/dolphin_stat|grep -v grep | awk {'print $1'} | awk {'print $1'}` ]; then
		echo "$NAME is already running."
	else
        echo "starting dolphinstat..."
        `nohup python $APP_DIR >>$ERR_DIR &` 
        PID=`ps ax | grep /srv/www/Broodling/dolphin_stat | grep -v grep | awk {'print $1'} | awk {'print $1'}`
        if [ $PID ]; then
            echo "pid$PID"
            sleep 1
        fi
	fi
}

function stop_worker()
{
    PID=`ps ax | grep /srv/www/Broodling/async/stat_worker.py | grep -v grep | awk {'print $1'} | awk {'print $1'}`
    for pid in ${PID[*]} 
    do
        kill -TERM $pid
        echo "killed stat worker pid:$pid"
    done
}

function start_worker()
{
    PID=`ps ax | grep /srv/www/Broodling/async/stat_worker.py | grep -v grep | awk {'print $1'} | awk {'print $1'}`
    if [ -n "$PID" ]; then
        echo "stat worker is already running."
    else
        echo "starting stat worker..."
        `nohup python /srv/www/Broodling/async/stat_worker.py >>$ERR_DIR &`
    fi
}

set -e

. /lib/lsb/init-functions

case "$1" in
	start)
		echo "Starting $DESC..."
		start_stat
		echo "Done."				
		;;
	stop)
		echo "Stopping $DESC..."
		stop_stat
		echo "Done."
		;;

	restart)
		echo "Restarting $DESC..."
		stop_stat
        sleep 4
		start_stat
		echo "Done."
		;;

    startw)
        echo "Starting worker..."
        start_worker
        echo "Done."
        ;;

    stopw)
        echo "Stop worker..."
        stop_worker
        echo "Done."
        ;;

	status)
		;;
	*)
		echo "Usage: $NAME {start|stop|restart|status}" >&2
		exit 1
		;;
esac

exit 0

