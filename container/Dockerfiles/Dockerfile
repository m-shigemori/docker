ARG ROS_DISTRO=jazzy

FROM ubuntu:26.04 AS base_lyrical
FROM ubuntu:24.04 AS base_jazzy
FROM ubuntu:22.04 AS base_humble

FROM base_${ROS_DISTRO}

ARG USER_NAME
ARG USER_ID
ARG GROUP_ID
ARG ROS_DISTRO
ARG ROS_DOMAIN_ID
ARG DEVICE=cpu
ARG CUDA_VER=12.8.1

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TZ=Asia/Tokyo

ENV USER_NAME=${USER_NAME} \
    HOME=/home/${USER_NAME}

ENV ROS_DISTRO=${ROS_DISTRO} \
    ROS_DOMAIN_ID=${ROS_DOMAIN_ID} \
    PYTHONDONTWRITEBYTECODE=1

ENV NVIDIA_VISIBLE_DEVICES=${NVIDIA_VISIBLE_DEVICES:-all} \
    NVIDIA_DRIVER_CAPABILITIES=${NVIDIA_DRIVER_CAPABILITIES:-all}

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://ftp.riken.jp/Linux/ubuntu/|g' /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || true \
 && sed -i 's|http://security.ubuntu.com/ubuntu|http://ftp.riken.jp/Linux/ubuntu/|g' /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || true

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    wget curl \
    ca-certificates gnupg2 \
    git gh python3-pip build-essential \
    nano gedit tree bash-completion \
    wl-clipboard \
    usbutils \
    iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN if [ "${DEVICE}" = "gpu" ]; then \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(echo ${ROS_DISTRO} | sed 's/lyrical/2604/;s/jazzy/2404/;s/humble/2204/')/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    && apt-get update && apt-get install -y --no-install-recommends \
       cuda-toolkit-$(echo ${CUDA_VER} | cut -d. -f1-2 | sed 's/\./-/') \
    && rm cuda-keyring_1.1-1_all.deb && rm -rf /var/lib/apt/lists/*; \
    fi

ENV PATH=/usr/local/cuda/bin:${PATH} \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

RUN install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | gpg --dearmor -o /etc/apt/keyrings/ros-archive-keyring.gpg \
 && chmod a+r /etc/apt/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-desktop ros-dev-tools \
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
 && chown ${USER_NAME}:${GROUP_ID} ${HOME}/.bash_aliases ${HOME}/.bashrc \
 && rm -rf /tmp/scripts

RUN rosdep init && rosdep update

USER ${USER_NAME}
WORKDIR ${HOME}/colcon_ws

CMD ["/bin/bash"]