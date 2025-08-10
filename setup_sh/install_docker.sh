#!/bin/bash
set -e

echo "パッケージリストを更新..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl

echo "DockerのGPG鍵とリポジトリを追加..."
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Docker Engineと関連ツールをインストール..."
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "現在のユーザーをdockerグループに追加..."
sudo usermod -aG docker $USER
newgrp docker

echo "Dockerサービスを有効化して起動..."
sudo systemctl enable docker
sudo systemctl start docker

echo "PyQt5をインストール..."
pip3 install PyQt5 --break-system-packages

echo "DockerのインストールとPyQt5の設定が完了
