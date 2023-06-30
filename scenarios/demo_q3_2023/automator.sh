#!/bin/bash

LOOP=0
delay=1

# require one parameter
if [ $# -lt 1 ]; then
    echo "Usage: $0 <pos_replay_file>"
    exit 1
fi

if [ $2 ]; then
    LOOP=$2
fi

if [ "$LOOP" -ne 0 ]; then
    echo "looping"
fi

# empty dictionary mapping node name to node ids
declare -A node_ids

while [ true ]; do
    # loop over all lines in file
    FILE=$1
    while read line; do
        # skip empty lines
        if [ -z "$line" ]; then
            continue
        fi

        # skip comments
        if [ "${line:0:1}" = "#" ]; then
            continue
        fi

        # if line starts with %delay, set delay
        if [ "${line:0:6}" = "%delay" ]; then
            delay=${line:7}
            echo "set delay: $delay"        
            continue
        fi

        if [ "${line}" = "-- STEP" ]; then
            sleep $delay
            continue
        fi
        # split line into array
        IFS=' ' read -r -a array <<< "$line"

        # get parameters
        node=${array[0]}
        # check if node existins in node_ids
        if [ -z "${node_ids[$node]}" ]; then
            echo "unknown id, retrieving from simulation..."
            NID=$(core-pos $node | grep Position | cut -d ":" -f 1 | xargs)
            # if not, add it
            node_ids[$node]=$NID
        fi
        node_id=${node_ids[$node]}
        x=${array[1]}
        y=${array[2]}
        command=${array[3]}

        # print parameters
        echo "node: $node ($node_id)"

        echo "pos: $x $y"
        core-pos $node_id $x $y
        #echo "heading: $heading"
        #echo "time: $time"    
    done < $FILE
    if [ $LOOP -eq 0 ]; then
        break
    fi    
done