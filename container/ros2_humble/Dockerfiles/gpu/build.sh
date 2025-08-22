#!/bin/bash

DIR=$(pwd)
str=`echo ${DIR} | awk -F "/" '{ print $(NF - 2) }'`

echo "CUDAバージョンを選択してください:"
echo "1. CUDA 12.2.2 (Ubuntu 22.04)"
echo "2. CUDA 12.5.1 (Ubuntu 22.04)"
echo "3. CUDA 12.8.1 (Ubuntu 22.04)"
echo "4. CUDA 12.9.1 (Ubuntu 22.04)"
read -p "選択肢の番号を入力してください (1-4): " choice

CUDA_VERSION_TAG=""
case $choice in
    1) CUDA_VERSION_TAG="12.2.2-cudnn" ;;
    2) CUDA_VERSION_TAG="12.5.1-cudnn" ;;
    3) CUDA_VERSION_TAG="12.8.1-cudnn" ;;
    4) CUDA_VERSION_TAG="12.9.1-cudnn" ;;
    *) echo "無効な選択です。終了します。" ; exit 1 ;;
esac

echo "選択されたCUDAバージョン: ${CUDA_VERSION_TAG}-devel-ubuntu22.04"

docker build \
    --tag sobits/${str} \
    --network host \
    --build-arg LOCAL_UID=$(id -u ${USER}) \
    --build-arg LOCAL_GID=$(id -g ${USER}) \
    --build-arg CUDA_BASE_IMAGE_TAG=${CUDA_VERSION_TAG} \
    .