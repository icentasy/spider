#!/bin/bash

pushd `dirname $0` > /dev/null
SCRIPT_DIR=`pwd -P`
popd > /dev/null

PHANTOMJS_URL=https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
PHANTOMJS_DIR=/usr/local/bin/
HIGHCHART_DIR=/var/app/data/
PHANTOMJS_SERVER_PORT=3005


install_deps(){
    mkdir /tmp/phantomjs
    apt-get build-dep phantomjs
    wget -O /tmp/phantomjs.tar.bz2 $PHANTOMJS_URL
    tar xvf /tmp/phantomjs.tar.bz2 -C /tmp/phantomjs --strip-components 1
    mkdir -p $PHANTOMJS_DIR
    mv /tmp/phantomjs/bin/phantomjs $PHANTOMJS_DIR
    rm -rf /tmp/phantomjs
    rm -rf /tmp/phantomjs.tar.bz2

    mkdir -p $HIGHCHART_DIR
    ln -s "$SCRIPT_DIR/highchart" $HIGHCHART_DIR
}

start_service(){
    nohup phantomjs "$HIGHCHART_DIR/highchart/highcharts-convert.js" -host 127.0.0.1 -port $PHANTOMJS_SERVER_PORT >/dev/null 2>&1 &
}

install_deps
start_service
