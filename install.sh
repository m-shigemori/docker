#!/bin/bash
set -e

sudo apt update
sudo apt install -y ca-certificates

sudo install -m 755 -d /etc/apt/keyrings

if ! command -v docker &> /dev/null; then
    bash setup/install_docker.sh
fi

if nvidia-smi &> /dev/null; then
    read -p "Install NVIDIA Container Toolkit? (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        bash setup/install_nvidia_docker.sh
    fi
fi

bash setup/setup_app.sh

if getent group docker > /dev/null; then
    if ! groups $USER | grep -q "\bdocker\b"; then
        sudo usermod -aG docker $USER
    fi
fi