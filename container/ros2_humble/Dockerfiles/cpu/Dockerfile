FROM ubuntu:22.04
LABEL maintainer="Shigemori Masao"

RUN echo "╔══╣ Install: ros2_humble_basic_ws:cpu (STARTING) ╠══╗"

ARG LOCAL_UID
ARG LOCAL_GID

ENV USER_NAME=sobits
ENV USER_ID=${LOCAL_UID:-1000}
ENV GROUP_ID=${LOCAL_GID:-1000}
ENV HOMEPATH=/home/sobits
ENV DEBCONF_NOWARNINGS=yes
ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    git \
    build-essential \
    python3-pip \
    locales \
    tzdata \
    tree && \
    rm -rf /var/lib/apt/lists/*

RUN echo "ja_JP.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen ja_JP.UTF-8 && \
    /usr/sbin/update-locale LANG=ja_JP.UTF-8

ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=Asia/Tokyo

RUN groupadd -g ${GROUP_ID} ${USER_NAME} && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash ${USER_NAME} && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME} && \
    chmod 0440 /etc/sudoers.d/${USER_NAME}

USER ${USER_NAME}

COPY install_ros2.sh ${HOMEPATH}/install_ros2.sh
RUN bash ${HOMEPATH}/install_ros2.sh --humble

COPY configure_shell.sh ${HOMEPATH}/configure_shell.sh
RUN bash ${HOMEPATH}/configure_shell.sh --ros2

RUN rm -f ${HOMEPATH}/install_ros2.sh ${HOMEPATH}/configure_shell.sh

USER root

RUN apt-get clean &&\
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/

ENV USER=${USER_NAME}
USER ${USER_NAME}

WORKDIR ${HOMEPATH}

RUN echo "╚══╣ Install: ros2_humble_basic_ws:cpu (FINISHED) ╠══╝"