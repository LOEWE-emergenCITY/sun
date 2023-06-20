#!/bin/sh
NODES=$(docker exec sun_core_1 bash -c "ls /tmp/*.xy" | egrep "[0-9]+")
# randomly select a node
node=$(echo $NODES | tr " " "\n" | shuf -n 1)

node=$(basename $node .xy)
echo "Sending bundle from $node to dtn://global/~txt"
docker exec sun_core_1 bash -c "cexec $node 'echo hello_world | dtnsend -r dtn://global/~txt'"
