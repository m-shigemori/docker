xhost +local:$USER >/dev/null

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

if [ -f "${DIR}/.env" ]; then
    export $(grep -v '^#' "${DIR}/.env" | xargs)
fi

export USE_GPU=${USE_GPU:-cpu}
export ROS_DISTRO=${ROS_DISTRO:-humble}
export USER_NAME=${USER_NAME:-sobits}
export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
export IMAGE_NAME="sobits/${NAME}"
export PARENT_DIR_NAME="${NAME}"

if [ -f "${HOME}/.gitconfig" ]; then
    cp "${HOME}/.gitconfig" "${DIR}/.gitconfig_sync"
else
    touch "${DIR}/.gitconfig_sync"
fi

if [ "${USE_GPU}" = "true" ] || [ "${USE_GPU}" = "gpu" ]; then
    export PROFILE="gpu"
    export USE_GPU="gpu"
else
    export PROFILE="cpu"
    export USE_GPU="cpu"
fi

echo "--- Starting with profile: ${PROFILE} ---"

mkdir -p "${DIR}/../src"

docker compose -p "${NAME}" -f "${DIR}/compose.yaml" --profile "${PROFILE}" up -d --build --remove-orphans
