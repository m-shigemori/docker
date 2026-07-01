#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$(dirname "$DIR")")"

SRC_DIR="${DIR}/../src"
mkdir -p "${SRC_DIR}"

export $(cat "${DIR}/.env" | xargs)

if [ -z "${UBUNTU_VER}" ]; then
    echo "Error: UBUNTU_VER is not set in .env" >&2
    exit 1
fi

if [ -z "${DEVICE}" ]; then
    echo "Error: DEVICE is not set in .env" >&2
    exit 1
fi

if [ "${UBUNTU_VER}" = "24.04" ]; then
    export ROS_DISTRO="jazzy"
elif [ "${UBUNTU_VER}" = "26.04" ]; then
    export ROS_DISTRO="lyrical"
else
    echo "Error: Unsupported UBUNTU_VER: ${UBUNTU_VER}" >&2
    exit 1
fi

export NAME="${NAME}"
export IMAGE_NAME="${USER_NAME}/${NAME}"

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"

XPROFILE="${HOME}/.xprofile"
XHOST_LINE="xhost +local:root > /dev/null 2>&1"

touch "${XPROFILE}"

if ! grep -qF "${XHOST_LINE}" "${XPROFILE}"; then
    echo "${XHOST_LINE}" >> "${XPROFILE}"
fi

xhost +local:root > /dev/null 2>&1

docker compose -p "${NAME}" --profile "${DEVICE}" up -d --build --remove-orphans