#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl
sudo apt install python3-pip -y

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER

sudo systemctl enable docker
sudo systemctl start docker

newgrp docker

pip3 install PyQt5 --break-system-packages

cat << 'EOF' >> ~/.bashrc

dockerpid="$(docker ps -q | head -1)"
function dock() {
  if [ "$1" == "-h" ]; then
    echo "Attaches this window as a new terminal (bash) instance to a running docker container"
    echo "Usage: 'dock' or 'dock {container_id_or_name}'"
    echo "If no ID is given, then attaches to first found process."
  elif [ $# -eq 0 ]; then
    echo "Running Docker Container: $dockerpid"
    docker exec -it "$dockerpid" /bin/bash
  elif [ "$1" != "-h" ]; then
    docker exec -it "$1" /bin/bash
  fi
}
if [[ "$dockerpid" != "" ]]; then
    dock
else
    echo "No docker container is running"
fi

alias ce='python3 ~/docker/scripts/main.py'
EOF