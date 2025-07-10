#!/bin/bash

DIR=$(pwd)
str=`echo ${DIR} | awk -F "/" '{ print $(NF - 2) }'`

docker build \
    --tag sobits/${str} \
    --network host \
    --build-arg LOCAL_UID=$(id -u ${USER}) \
    --build-arg LOCAL_GID=$(id -g ${USER}) \
    .