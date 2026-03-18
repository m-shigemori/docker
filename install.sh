#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings

if ! command -v docker &> /dev/null; then
    bash setup/install_docker.sh
fi

if lspci | grep -i nvidia &> /dev/null; then
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
