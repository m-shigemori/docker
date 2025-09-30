#!/bin/bash

DIR=$(pwd)
STR=$(echo "${DIR}" | awk -F "/" '{ print $(NF - 2) }')
IMAGE_NAME="sobits/${STR}"

cd "$(pwd)/../../"

if [ ! -d "src" ]; then
    mkdir -p src
fi
xhost +local:${USER}

VIDEO_DEVICES=""
for dev in /dev/video*; do
    [ -e "$dev" ] && VIDEO_DEVICES="$VIDEO_DEVICES --device $dev"
done

docker run -it \
    --gpus all \
    --device /dev/snd \
    --device /dev/dri \
    $VIDEO_DEVICES \
    --group-add audio \
    --group-add video \
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