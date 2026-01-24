#!/bin/bash

xhost +local:$USER > /dev/null

export SCRIPT_DIR=$(cd $(dirname "$0"); pwd)
export PARENT_DIR_NAME=$(basename "$(dirname "$SCRIPT_DIR")")

if [ -f "${SCRIPT_DIR}/.env" ]; then
    export $(grep -v '^#' "${SCRIPT_DIR}/.env" | xargs)
fi

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
export ROS_DISTRO=${ROS_DISTRO:-humble}
export IMAGE_NAME="sobits/${PARENT_DIR_NAME}"

if [ "$USE_GPU" = "true" ]; then
    export PROFILE="gpu"
else
    export PROFILE="cpu"
fi

mkdir -p "${SCRIPT_DIR}/../src"

docker compose -p "${PARENT_DIR_NAME}" -f "${SCRIPT_DIR}/compose.yaml" --profile "${PROFILE}" up -d --build --remove-orphans