#!/bin/bash

DIR=$(pwd)
STR=$(echo "${DIR}" | awk -F "/" '{ print $(NF - 2) }')
IMAGE_NAME="sobits/${STR}"

cd "$(pwd)/../../"

mkdir -p src
xhost +local:${USER}

docker run -it \
    --device /dev/snd \
    --group-add audio \
    --env CONTAINER_NAME="${STR}" \
    --env DISPLAY="${DISPLAY}" \
    --env PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
    --volume /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse \
    --volume /etc/machine-id:/etc/machine-id:ro \
    --volume /etc/udev/rules.d/:/etc/udev/rules.d/ \
    --volume /dev/bus/usb:/dev/bus/usb \
    --volume /dev/snd:/dev/snd \
    --volume "$(pwd)/src:/home/sobits/colcon_ws/src/" \
    --net host \
    --privileged \
    --shm-size=1g \
    --name "${STR}" \
    --user $(id -u):$(id -g) \
    "${IMAGE_NAME}" \
    /bin/bash
