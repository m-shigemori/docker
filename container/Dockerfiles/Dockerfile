ARG ROS_DISTRO=humble
FROM osrf/ros:${ROS_DISTRO}-desktop-full

ARG LOCAL_UID=1000
ARG LOCAL_GID=1000
ARG ROS_DOMAIN_ID=53

ENV USER_NAME=sobits \
    HOME=/home/sobits \
    DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    TZ=Asia/Tokyo \
    ROS_DOMAIN_ID=${ROS_DOMAIN_ID} \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo tree bash-completion usbutils nano gh python3-pip xsel \
    libasound2-plugins libportaudio2 \
 && rm -rf /var/lib/apt/lists/*

RUN echo "[install]\nbreak-system-packages = true" \
    > /etc/pip.conf

RUN if [ $(getent group ${LOCAL_GID}) ]; \
    then \
        groupmod -n ${USER_NAME} $(getent group ${LOCAL_GID} | cut -d: -f1); \
    else \
        groupadd -g ${LOCAL_GID} ${USER_NAME}; \
    fi \
 && if [ $(getent passwd ${LOCAL_UID}) ]; \
    then \
        userdel -r $(getent passwd ${LOCAL_UID} | cut -d: -f1); \
    fi \
 && useradd -u ${LOCAL_UID} -g ${LOCAL_GID} -m -s /bin/bash ${USER_NAME} \
 && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} \
 && chmod 0440 /etc/sudoers.d/${USER_NAME}

RUN mkdir -p ${HOME}/colcon_ws/src ${HOME}/.ros/log \
 && chown -R ${LOCAL_UID}:${LOCAL_GID} ${HOME}

USER ${USER_NAME}

RUN rosdep update

RUN cat <<EOF >> ${HOME}/.bashrc

export EDITOR=nano
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}

source /opt/ros/${ROS_DISTRO}/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

if [ -f ~/colcon_ws/install/setup.bash ];
then
    source ~/colcon_ws/install/setup.bash
fi
EOF

RUN cat <<'EOF' > ${HOME}/.bash_aliases
export PS1="\[\e[1;36;48;5;232m\]${CONTAINER_NAME:-docker}\[\e[0m\]\[\e[01;32m\]@\u\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "

alias source_bashrc="source ~/.bashrc"
alias pip3='python3 -m pip'
alias copy='xsel -bi'

alias roscd="cd ~/colcon_ws"
alias cb="cd ~/colcon_ws && colcon build --symlink-install"
alias cbp="cd ~/colcon_ws && colcon build --symlink-install --packages-select"

alias rt="ros2 topic list"
alias rn="ros2 node list"
alias rs="ros2 service list"
alias ra="ros2 action list"
alias re="ros2 topic echo"
EOF

WORKDIR ${HOME}
CMD ["/bin/bash"]