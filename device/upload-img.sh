#!/bin/bash

UPLOAD_FOLDER="/home/pi/everysecond/upload"
TARGET_FOLDER="gs://bucket.everysecond.live/customer0001/rpi0001/"

while :
do
    WLAN=`ifconfig | grep wlan0`
    # echo "Network is $WLAN"
    if [ "$WLAN" != "" ]
    then
        OLDFILE=`ls -t $UPLOAD_FOLDER | tail -1`
        mv $UPLOAD_FOLDER/new/* $UPLOAD_FOLDER/
        OLDEST=$UPLOAD_FOLDER/$OLDFILE

        if [[ "$OLDEST" == *".jpg"* ]]
        then
            echo "uploading to cloud"
            gsutil -m cp $UPLOAD_FOLDER/*.jpg $TARGET_FOLDER
            if [ $(echo $?) == 0 ]
            then
                echo "removing file $OLDEST"
                rm $UPLOAD_FOLDER/*.jpg
                sleep 10s
            fi
        else
            sleep 5s
        fi
    fi
done
