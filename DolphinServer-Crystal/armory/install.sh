#!/bin/bash

function install_pip()
{
    apt-get install libmysqlclient-dev
    pip install mysql-python
	pip install simplejson
	pip install requests
	pip install openpyxl
	pip install geoip2
	pip install redis
	pip install functools
	pip install sqlalchemy
	pip install pymongo
}

function install_data()
{
	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz
	if [ ! -d /data ];then
		mkdir /data
	fi
	mv GeoLite2-City.mmdb.gz /data
	mv GeoLite2-Country.mmdb.gz /data
	cd /data
	gzip -d GeoLite2-City.mmdb.gz
	gzip -d GeoLite2-Country.mmdb.gz
	cd -
}

install_pip
install_data
