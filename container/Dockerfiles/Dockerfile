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

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TZ=Asia/Tokyo

ENV USER_NAME=${USER_NAME} \
    HOME=/home/${USER_NAME}

ENV ROS_DISTRO=${ROS_DISTRO} \
    ROS_DOMAIN_ID=${ROS_DOMAIN_ID} \
    PYTHONDONTWRITEBYTECODE=1

RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://ftp.riken.jp/Linux/ubuntu/|g' /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || true \
 && sed -i 's|http://security.ubuntu.com/ubuntu|http://ftp.riken.jp/Linux/ubuntu/|g' /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources 2>/dev/null || true

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo
#     wget curl \
#     git gh \
#     nano gedit \
#     tree usbutils \
#     bash-completion \
#     wl-clipboard \
#     python3-pip \
#     iproute2 iputils-ping \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

RUN if getent passwd ${USER_ID} > /dev/null; then userdel -r $(getent passwd ${USER_ID} | cut -d: -f1); fi \
 && if getent group ${GROUP_ID} > /dev/null; then groupdel $(getent group ${GROUP_ID} | cut -d: -f1); fi \
 && groupadd -g ${GROUP_ID} ${USER_NAME} \
 && useradd -m -u ${USER_ID} -g ${GROUP_ID} -s /bin/bash ${USER_NAME} \
 && echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} \
 && chmod 0440 /etc/sudoers.d/${USER_NAME}

COPY scripts/ /tmp/scripts/

RUN cat /tmp/scripts/.bash_aliases >> ${HOME}/.bash_aliases \
 && cat /tmp/scripts/.bashrc_custom >> ${HOME}/.bashrc \
 && chown ${USER_NAME}:${GROUP_ID} ${HOME}/.bash_aliases ${HOME}/.bashrc \
 && rm -rf /tmp/scripts

USER ${USER_NAME}
WORKDIR ${HOME}/colcon_ws

CMD ["/bin/bash"]