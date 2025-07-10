#!/bin/bash

# 現在のディレクトリパスからイメージ名を自動生成
DIR=$(pwd)
str=`echo ${DIR} | awk -F "/" '{ print $(NF - 2) }'`

# Dockerイメージをビルド
docker build \
    --tag sobits/${str} \
    --network host \
    --build-arg LOCAL_UID=$(id -u ${USER}) \
    --build-arg LOCAL_GID=$(id -g ${USER}) \
    .