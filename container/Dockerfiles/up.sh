#!/bin/bash

xhost +local:$USER >/dev/null

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
export ROS_DISTRO=${ROS_DISTRO:-humble}
export IMAGE_NAME="sobits/${NAME}"
export PARENT_DIR_NAME="${NAME}"
export GITHUB_TOKEN=$(gh auth token)

[ "$USE_GPU" = "true" ] && PROFILE="gpu" || PROFILE="cpu"

mkdir -p "${DIR}/../src"

docker compose -p "${NAME}" -f "${DIR}/compose.yaml" \
  --profile "${PROFILE}" up -d --build --remove-orphans