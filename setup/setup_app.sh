#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y python3-pip fzf

pip3 install PyQt5 --break-system-packages

cat << 'EOF' >> ~/.bashrc

CONTAINER_LIST=$(docker ps --format "{{.ID}}\t{{.Names}}")
CONTAINER_COUNT=$(echo "$CONTAINER_LIST" | grep -c .)

if [ "$CONTAINER_COUNT" -eq 1 ]; then
    docker exec -it $(echo "$CONTAINER_LIST" | cut -f1) /bin/bash

elif [ "$CONTAINER_COUNT" -gt 1 ]; then
    SELECTED_CONTAINER=$(echo "$CONTAINER_LIST" | \
        fzf \
            --height=$((CONTAINER_COUNT + 1)) \
            --layout=reverse-list \
            --no-info \
            --no-sort \
            --border=none \
            --prompt="")

    if [ -n "$SELECTED_CONTAINER" ]; then
        docker exec -it $(echo "$SELECTED_CONTAINER" | cut -f1) /bin/bash
    fi
fi

alias ce='python3 ~/docker/control/app.py'
fi
EOF