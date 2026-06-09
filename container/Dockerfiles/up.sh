#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$(dirname "$DIR")")"

SRC_DIR="${DIR}/../src"
mkdir -p "${SRC_DIR}"

export $(cat "${DIR}/.env" | xargs)

if [ "${UBUNTU_VER}" = "24.04" ]; then
    export ROS_DISTRO="jazzy"
elif [ "${UBUNTU_VER}" = "26.04" ]; then
    export ROS_DISTRO="lyrical"

export NAME="${NAME}"
export IMAGE_NAME="${USER_NAME}/${NAME}"

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"

docker compose -p "${NAME}" --profile "${DEVICE}" up -d --build --remove-orphans
