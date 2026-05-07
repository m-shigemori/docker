#!/bin/bash

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

SRC_DIR="${DIR}/../src"
mkdir -p "${SRC_DIR}"

export $(grep -v '^#' "${DIR}/.env" | xargs)

export NAME=${NAME}
export IMAGE_NAME="${USER_NAME}/${NAME}"

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

docker compose --profile "${DEVICE}" up -d --build
