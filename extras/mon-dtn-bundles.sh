#!/bin/sh

docker exec -it sun_core_1 watch "cea 'dtnquery bundles | grep -e dtn: -e ipn: | wc -l'"
