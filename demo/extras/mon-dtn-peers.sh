#!/bin/sh

docker exec -it demo_core_1 watch "cea 'dtnquery peers | grep addr | wc -l'"
