xhost +local:$USER >/dev/null

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

if [ -f "${DIR}/.env" ]; then
    export $(grep -v '^#' "${DIR}/.env" | xargs)
fi

export USE_GPU=${USE_GPU:-cpu}
export ROS_DISTRO=${ROS_DISTRO:-humble}
export USER_NAME=${USER_NAME:-peru}
export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
export IMAGE_NAME="peru/${NAME}"
export PARENT_DIR_NAME="${NAME}"

if [ "${USE_GPU}" = "true" ] || [ "${USE_GPU}" = "gpu" ]; then
    export PROFILE="gpu"
    export USE_GPU="gpu"
else
    export PROFILE="cpu"
    export USE_GPU="cpu"
fi

echo "--- Starting with profile: ${PROFILE} ---"

SRC_DIR="${DIR}/../src"
mkdir -p "${SRC_DIR}"

if [ ! -d "${SRC_DIR}/gemini_mcp_suite" ]; then
    echo "--- Cloning gemini_mcp_suite into ${SRC_DIR} ---"
    git clone https://github.com/m-shigemori/gemini_mcp_suite.git "${SRC_DIR}/gemini_mcp_suite"
fi

docker compose -p "${NAME}" -f "${DIR}/compose.yaml" --profile "${PROFILE}" up -d --build --remove-orphans
