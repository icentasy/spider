#!/bin/bash
#
# This scripts is used to restart the application.
# This scripts is required for all projects.
#
#
# Author : kunli
#

pid=`ps ax | grep dolphin_stat | grep -v grep | awk {'print $1'} | awk {'print $1'}`

if [ $pid ]; then
	service Broodling restart
else
	service Broodling start
fi
