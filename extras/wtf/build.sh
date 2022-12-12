#!/bin/sh

curl -o Dockerfile.build https://raw.githubusercontent.com/wtfutil/wtf/master/Dockerfile.build
docker build -f Dockerfile.build -t wtfutil --build-arg=version=v0.41.0 .
docker create --name wtf_build wtfutil
docker cp wtf_build:/usr/local/bin/wtfutil .
docker rm wtf_build
rm Dockerfile.build