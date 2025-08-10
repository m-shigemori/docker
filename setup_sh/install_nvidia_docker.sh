#!/bin/bash
set -e

echo "Dockerをインストール..."
./install_docker.sh

echo "NVIDIA Container ToolkitのリポジトリとGPG鍵を追加..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

echo "NVIDIA Container Toolkitをインストール..."
sudo apt-get update -y
sudo apt-get install -y nvidia-container-toolkit

echo "DockerとNVIDIA Container Toolkitを統合..."
sudo nvidia-ctk runtime configure --runtime=docker

echo "コンテナ設定ファイルを編集..."
sudo sed -i -e 's/^#no-cgroups = .*/no-cgroups = false/' -e 's/^no-cgroups = .*/no-cgroups = false/' /etc/nvidia-container-runtime/config.toml

echo "Dockerサービスを再起動..."
sudo systemctl restart docker

echo "NVIDIA Dockerのセットアップが完了"
