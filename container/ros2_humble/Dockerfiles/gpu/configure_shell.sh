#!/bin/bash

ROS_VERall=("ros2")
SELECTED_ROS_VER=$1
SELECTED_ROS_VER=${SELECTED_ROS_VER//-}

check_ros_ver() {
    local ver_to_check=$1
    if [[ ! " ${ROS_VERall[*]} " =~ " ${ver_to_check} " ]]; then
        echo "Error: Please select from the following ROS versions:"
        echo "       ${ROS_VERall[*]}"
        echo "       Example: bash $(basename "$0") --ros2"
        exit 1
    fi
}

check_ros_ver "${SELECTED_ROS_VER}"

echo "╔══╣ ROS2 Environment Aliases Setup (Starting) ╠══╗"

CURRENT_USER=$(whoami)
echo "Current user: ${CURRENT_USER}"

ALIAS_FILE="/home/${CURRENT_USER}/.bash_aliases"
echo "Alias file: ${ALIAS_FILE}"

if [ ! -f "${ALIAS_FILE}" ]; then
    touch "${ALIAS_FILE}"
    echo "Created new alias file: ${ALIAS_FILE}"
else
    echo "Appending to existing alias file: ${ALIAS_FILE}"
fi

echo "alias pip='python -m pip'" >> "${ALIAS_FILE}"
echo "alias pip3='python3 -m pip'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

echo "alias ls='ls --color=auto'" >> "${ALIAS_FILE}"
echo "alias ll='ls -alF'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

echo "alias roscd='cd ~/colcon_ws/src'" >> "${ALIAS_FILE}"
echo "alias ..='cd ..'" >> "${ALIAS_FILE}"
echo "alias ...='cd ../..'" >> "${ALIAS_FILE}"
echo "alias ....='cd ../../..'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

echo "alias cp='cp -i'" >> "${ALIAS_FILE}"
echo "alias mv='mv -i'" >> "${ALIAS_FILE}"
echo "alias rm='rm -i'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

echo "export PYTHONDONTWRITEBYTECODE=1" >> "${ALIAS_FILE}"
echo "export PS1='\[\e[1;36;40m\]\$CONTAINER_NAME\[\e[0m\\] \${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> "${ALIAS_FILE}"
echo "export EDITOR='nano'" >> "${ALIAS_FILE}"

if [ -f "${ALIAS_FILE}" ]; then
    echo "Configuration written to: ${ALIAS_FILE}"
    echo "File size: $(wc -l < "${ALIAS_FILE}") lines"
    ls -la "${ALIAS_FILE}"
else
    echo "Error: Failed to create file: ${ALIAS_FILE}"
fi

echo "╚══╣ ROS2 Environment Aliases Setup (Completed) ╠══╝"