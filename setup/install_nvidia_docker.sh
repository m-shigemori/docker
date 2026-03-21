#!/bin/bash
set -e

if [ ! -f /etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg ]; then
    curl -fsSLk https://nvidia.github.io/libnvidia-container/gpgkey | \
        sudo gpg --dearmor -o /etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg
    sudo chmod a+r /etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg
fi

if [ ! -f /etc/apt/sources.list.d/nvidia-container-toolkit.list ]; then
    curl -sLk https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
fi

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
