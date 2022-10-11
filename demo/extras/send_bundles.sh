#!/bin/sh

for node in $(docker exec demo_core_1 bash -c "ls /tmp/*.xy" | egrep "[0-9]+"); do
  node=$(basename $node .xy)
  echo "Sending bundle from $node to dtn://global/~txt"
  docker exec demo_core_1 bash -c "cexec $node 'echo hello_world | dtnsend -r dtn://global/~txt'"
done
