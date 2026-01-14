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
    sudo tree bash-completion usbutils nano gh\
 && rm -rf /var/lib/apt/lists/*

RUN if id -u ${LOCAL_UID} >/dev/null 2>&1; then \
        userdel -r $(id -nu ${LOCAL_UID}) 2>/dev/null || true; \
    fi \
 && useradd -u ${LOCAL_UID} -m -s /bin/bash ${USER_NAME} \
 && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} \
 && chmod 0440 /etc/sudoers.d/${USER_NAME} \
 && mkdir -p ${HOME}/colcon_ws/src \
 && chown -R ${LOCAL_UID}:${LOCAL_GID} ${HOME}/colcon_ws

RUN cat <<'EOF' >> ${HOME}/.bashrc
source /etc/bash_completion
source /opt/ros/${ROS_DISTRO}/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
if [ -f ~/colcon_ws/install/setup.bash ]; then source ~/colcon_ws/install/setup.bash; fi
export EDITOR=nano
if [ -f ~/.bash_aliases ]; then . ~/.bash_aliases; fi
EOF

RUN cat <<'EOF' > ${HOME}/.bash_aliases
export PS1="\[\e[1;36m\]$CONTAINER_NAME@\u\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "
alias source_bashrc="source ~/.bashrc"
alias roscd="cd ~/colcon_ws"
alias cb="cd ~/colcon_ws && colcon build --symlink-install"
alias cbp="cd ~/colcon_ws && colcon build --symlink-install --packages-select"
alias rt="ros2 topic list"
alias rn="ros2 node list"
alias rs="ros2 service list"
alias ra="ros2 action list"
EOF

RUN chown ${LOCAL_UID}:${LOCAL_GID} ${HOME}/.bashrc ${HOME}/.bash_aliases

USER ${USER_NAME}
WORKDIR ${HOME}
CMD ["/bin/bash"]