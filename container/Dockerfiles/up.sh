#!/bin/bash

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

SRC_DIR="${DIR}/../src"
mkdir -p "${SRC_DIR}"

[ ! -d "${SRC_DIR}/gemini_mcp_suite" ] && git clone -q https://github.com/m-shigemori/gemini_mcp_suite.git "${SRC_DIR}/gemini_mcp_suite"

export $(grep -v '^#' "${DIR}/.env" | xargs)

export NAME=${NAME}
export IMAGE_NAME="${USER_NAME}/${NAME}"

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

docker compose -p "${NAME}" --profile "${DEVICE}" up -d --build --remove-orphans