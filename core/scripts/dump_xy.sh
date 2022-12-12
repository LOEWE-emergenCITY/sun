#!/bin/sh

for i in /tmp/*.xy
do
    XY=$(cat $i | sed 's/\.[0-9]*//g')
    X=$(echo $XY | cut -d, -f1)
    Y=$(echo $XY | cut -d, -f2)
    printf '%-10s' $(basename $i .xy)
    printf '%-10s' "$X"
    printf '%-10s' "$Y"
    echo
done | grep -v WiFi