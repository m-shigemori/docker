ARG ROS_DISTRO=jazzy
ARG CUDA_VER=12.8.1

FROM nvidia/cuda:${CUDA_VER}-cudnn-devel-ubuntu24.04 AS ubuntu24
FROM nvidia/cuda:${CUDA_VER}-cudnn-devel-ubuntu22.04 AS ubuntu22

ARG ROS_DISTRO
FROM ubuntu24 AS jazzy
FROM ubuntu22 AS humble
FROM ${ROS_DISTRO}

ARG ROS_DISTRO
ARG LOCAL_UID=1000
ARG LOCAL_GID=1000
ARG ROS_DOMAIN_ID=53
ARG USER_NAME=sobits

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TZ=Asia/Tokyo \
    PYTHONDONTWRITEBYTECODE=1 \
    USER_NAME=${USER_NAME} \
    HOME=/home/${USER_NAME} \
    ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg2 lsb-release sudo tree bash-completion usbutils nano gedit gh \
    python3-pip xsel libasound2-plugins libportaudio2 \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu \
    $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    > /etc/apt/sources.list.d/ros2.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-desktop ros-dev-tools python3-rosdep \
 && rm -rf /var/lib/apt/lists/* \
 && echo "[install]\nbreak-system-packages = true" > /etc/pip.conf

RUN if getent passwd ${LOCAL_UID}; then userdel -r $(getent passwd ${LOCAL_UID} | cut -d: -f1); fi \
 && if getent group ${LOCAL_GID}; then groupdel $(getent group ${LOCAL_GID} | cut -d: -f1); fi \
 && groupadd -g ${LOCAL_GID} ${USER_NAME} \
 && useradd -u ${LOCAL_UID} -g ${LOCAL_GID} -m -s /bin/bash ${USER_NAME} \
 && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} \
 && chmod 0440 /etc/sudoers.d/${USER_NAME} \
 && mkdir -p ${HOME}/colcon_ws/src ${HOME}/.ros/log \
 && chown -R ${LOCAL_UID}:${LOCAL_GID} ${HOME}

RUN printf "%s\n" \
    "export EDITOR=nano" \
    "export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}" \
    "source /opt/ros/${ROS_DISTRO}/setup.bash" \
    "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" \
    "[ -f ~/colcon_ws/install/setup.bash ] && source ~/colcon_ws/install/setup.bash" \
    >> ${HOME}/.bashrc

RUN cat <<'EOF' >> ${HOME}/.bash_aliases
export PS1="\[\e[1;36;48;5;232m\]\${CONTAINER_NAME:-docker}\[\e[0m\]\[\e[01;32m\]@\u\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "
alias copy="xsel -bi"

alias roscd="cd ~/colcon_ws"
alias source_bashrc="source ~/.bashrc"
alias cb="roscd && colcon build --symlink-install"
alias cbp="roscd && colcon build --symlink-install --packages-select"
alias rt="ros2 topic list"
alias rn="ros2 node list"
alias rs="ros2 service list"
alias ra="ros2 action list"
alias re="ros2 topic echo"

alias ghl='gh repo list'
alias ghc='gh repo clone'
alias ghurl='gh repo view --json url -q .url'
EOF

RUN rosdep init && rosdep update

USER ${USER_NAME}
WORKDIR ${HOME}

CMD ["/bin/bash"]