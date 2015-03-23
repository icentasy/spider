#!/bin/bash
echo -----Copy source code to site folder-------
if [ ! -d /srv/www/ ]
then
	sudo mkdir -p /srv/www/
fi
LOGROOT=/srv/www/Broodling/log
CONFROOT=/srv/www/Broodling/conf

if [ -f $CONFROOT/log_record.xml ]
then
    cp $CONFROOT/log_record.xml /tmp/
fi

sudo cp -rf Broodling /srv/www/
sudo cp -rf ./scripts /srv/www/Broodling/
sudo chown www-data:adm -R /srv/www
if [ ! -d $LOGROOT ]
then
    sudo mkdir -p $LOGROOT
    sudo touch $LOGROOT/parse.log
    sudo chown -R :www-data $LOGROOT
    sudo chmod -R a+w $LOGROOT
    sudo chmod -R a+w $LOGROOT/parse.log
fi

if [ -f /tmp/log_record.xml ]
then
    mv /tmp/log_record.xml $CONFROOT/log_record.xml
fi

sudo chmod -R a+w $CONFROOT
sudo chmod -R a+w $CONFROOT/*
