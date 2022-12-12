#!/bin/sh

docker exec -it sun_core_1 watch "cea 'dtnquery peers | grep addr | wc -l'"
