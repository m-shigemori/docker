FROM ubuntu:26.04

ARG GROUP_ID
ARG USER_ID
ARG USER_NAME

ARG DEVICE
ARG CUDA_VER

ARG ROS_DOMAIN_ID

ENV USER_NAME=${USER_NAME} \
    HOME=/home/${USER_NAME} \
    PYTHONDONTWRITEBYTECODE=1

ENV LANG=C.UTF-8 \
    TZ=Asia/Tokyo

ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all \
    PATH=/usr/local/cuda/bin:${PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    wget curl gnupg2 software-properties-common \
    git gh python3-pip \
    nano gedit tree \
    wl-clipboard \
    usbutils \
    iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN if [ "${DEVICE}" = "gpu" ]; then \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2604/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && CUDA_TAG="$(echo "$CUDA_VER" | cut -d . -f 1-2 | tr '.' '-')" \
    && apt-get update && apt-get install -y --no-install-recommends cuda-toolkit-${CUDA_TAG} \
    && rm cuda-keyring_1.1-1_all.deb && rm -rf /var/lib/apt/lists/*; \
    fi

RUN export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') \
 && curl -L -o /tmp/ros2-apt-source.deb \
    "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" \
 && dpkg -i /tmp/ros2-apt-source.deb \
 && rm /tmp/ros2-apt-source.deb \
# RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common \
#  && add-apt-repository universe \
#  && export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') \
#  && curl -L -o /tmp/ros2-apt-source.deb \
#     "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" \
#  && dpkg -i /tmp/ros2-apt-source.deb \
#  && rm /tmp/ros2-apt-source.deb \
 && apt-get update && apt-get install -y --no-install-recommends \
    ros-lyrical-desktop ros-dev-tools \
 && rm -rf /var/lib/apt/lists/*

RUN if getent passwd ${USER_ID} > /dev/null; then userdel -r $(getent passwd ${USER_ID} | cut -d: -f1); fi \
 && if getent group ${GROUP_ID} > /dev/null; then groupdel $(getent group ${GROUP_ID} | cut -d: -f1); fi \
 && groupadd -g ${GROUP_ID} ${USER_NAME} \
 && useradd -m -u ${USER_ID} -g ${GROUP_ID} -s /bin/bash ${USER_NAME} \
 && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} \
 && chmod 0440 /etc/sudoers.d/${USER_NAME} \
 && mkdir -p ${HOME}/colcon_ws/src ${HOME}/.ros/log \
 && chown -R ${USER_ID}:${GROUP_ID} ${HOME}

COPY scripts/ /tmp/scripts/
RUN cat /tmp/scripts/.bash_aliases >> ${HOME}/.bash_aliases \
 && cat /tmp/scripts/.bashrc_custom >> ${HOME}/.bashrc \
 && echo "source /opt/ros/lyrical/setup.bash" >> ${HOME}/.bashrc \
 && echo "export ROS_DOMAIN_ID=${ROS_DOMAIN_ID}" >> ${HOME}/.bashrc \
 && chown ${USER_NAME}:${GROUP_ID} ${HOME}/.bash_aliases ${HOME}/.bashrc \
 && rm -rf /tmp/scripts

RUN mkdir -p ${HOME}/.config/pip \
 && echo -e "[global]\nbreak-system-packages = true" > ${HOME}/.config/pip/pip.conf \
 && chown -R ${USER_ID}:${GROUP_ID} ${HOME}/.config

RUN rosdep init && rosdep update

USER ${USER_NAME}
WORKDIR ${HOME}/colcon_ws

CMD ["/bin/bash"]