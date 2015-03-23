#!/bin/bash

DATE_STR=20140323

while [ $DATE_STR -gt 20140301 ]
do
    DATE_STR=`expr $DATE_STR - 1`
    echo "begin get $DATE_STR from s3..."
    `s3cmd get -c "/home/ubuntu/.s3cfg" s3://logserver/input/dolphinsync-en/nginx-access/$DATE_STR/nginx.access.log.lzo ./`
    echo "finish get $DATE_STR from s3, begin depress..."
    `lzop -d ./nginx.access.log.lzo`
    echo "finish depress, begin parse offline..."
    rm nginx.access.log.lzo

    mv ./nginx.access.log ./nginx.access.log.lzo.$DATE_STR

    `python /tmp/offline_nginx.py ./nginx.access.log.lzo.$DATE_STR >> ./offline.log`

    rm ./nginx.access.log.lzo.$DATE_STR 
    echo "finish parse offline of $DATE_STR"
done
