#!/bin/bash

DIR=$(pwd)
str=`echo ${DIR} | awk -F "/" '{ print $(NF - 2) }'`

cd $(pwd)/../../

if [ ! -d "src" ]; then
    mkdir -p src
fi

xhost +local:${USER}

docker run -it \
    --device /dev/snd \
    --env CONTAINER_NAME=${str} \
    --env DISPLAY=${DISPLAY} \
    --env PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
    --volume /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse \
    --volume /etc/udev/rules.d/:/etc/udev/rules.d/ \
    --volume $(pwd)/src/:/home/sobits/colcon_ws/src/ \
    --shm-size=1g \
    --net host \
    --name ${str} \
    --privileged \
    --user $(id -u):$(id -g) \
    sobits/${str} \
    /bin/bash