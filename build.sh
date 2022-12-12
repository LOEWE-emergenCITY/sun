#!/bin/sh

# check if file exists
if [ ! -f "docker-compose.yml" ]; then
    echo "no config found, generating one..."
    cat templates/docker-compose.yml.TEMPLATE | sed -e 's/SHAREDDIR/.\/shared/g' >docker-compose.yml
fi
docker-compose build
