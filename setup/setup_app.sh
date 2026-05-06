#!/bin/bash
set -e

sudo apt-get install -y python3-pyqt5 fzf

PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)

MARKER="# ContainerExecuter Setup"
if ! grep -q "$MARKER" ~/.bashrc; then
    cat << EOF >> ~/.bashrc

$MARKER
function dock()
{
  if [ "\$1" == "-h" ]; then
    echo "Usage: 'dock' (interactive selection) or 'dock {container_id_or_name}'"
    return
  fi

  if [ \$# -gt 0 ]; then
    docker exec -it "\$1" /bin/bash
    return
  fi

  local containers=\$(docker ps --format "{{.ID}}\t{{.Names}}\t{{.Image}}")

  if [ -z "\$containers" ]; then
    echo "No running containers found."
    return
  fi

  local count=\$(echo "\$containers" | wc -l)

  if [ "\$count" -eq 1 ]; then
    local target=\$(echo "\$containers" | awk '{print \$1}')
    echo "Attaching to: \$target"
    docker exec -it "\$target" /bin/bash
    return
  fi

  local target=\$(echo "\$containers" | fzf --height 40% --reverse --header "Select a container to attach" --prompt "> " | awk '{print \$1}')

  if [ -n "\$target" ]; then
    docker exec -it "\$target" /bin/bash
  fi
}

alias ce='python3 $PROJECT_DIR/main.py'
EOF
fi
