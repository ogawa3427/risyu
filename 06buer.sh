#!/bin/bash
while true; do
    asof=$(curl https://kurisyushien.org/api | sed 's/\\n/\n/g' | grep "valid" | sed 's/ //g' | sed 's|/||g' | sed 's/\\tvalid//g')
    echo $asof
    curl https://kurisyushien.org/api > ./csvs/"$asof"
    sleep 51
done