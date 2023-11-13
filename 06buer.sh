#!/bin/bash
while true; do
    asof=$(curl  http://20.78.138.195:5000/api | sed 's/","/\n/g' | grep "asof" | sed 's/[^0-9]//g' | sed 's/$/.csv/')
    echo $asof
    curl http://20.78.138.195:5000/api > ./csvs/"$asof"
    sleep 51
done