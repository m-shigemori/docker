xhost +local:$USER >/dev/null

DIR=$(cd $(dirname "$0"); pwd)
NAME=$(basename "$(dirname "$DIR")")

if [ -f "${DIR}/.env" ]; then
    export $(grep -v '^#' "${DIR}/.env" | xargs)
fi

export USER_NAME=${USER_NAME:-sobits}
export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
export GITHUB_TOKEN=$(gh auth token)
export DISPLAY=${DISPLAY}

export ROS_DISTRO=${ROS_DISTRO:-humble}
export IMAGE_NAME="sobits/${NAME}"
export PARENT_DIR_NAME="${NAME}"

[ "$USE_GPU" = "true" ] && PROFILE="gpu" || PROFILE="cpu"

mkdir -p "${DIR}/../src"

docker compose -p "${NAME}" -f "${DIR}/compose.yaml" --profile "${PROFILE}" up -d --build --remove-orphans