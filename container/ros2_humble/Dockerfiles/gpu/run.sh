#!/bin/bash

DIR=$(pwd)
str=`echo ${DIR} | awk -F "/" '{ print $(NF - 2) }'`

# 実行するイメージ名を sobits/${str} に固定 (build.shで設定されたタグと一致)
IMAGE_NAME="sobits/${str}"

cd $(pwd)/../../

if [ ! -d "src" ]; then
    mkdir -p src
fi

xhost +local:${USER}

docker run -it \
    --gpus all \
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