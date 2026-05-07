export PS1="\[\e[1;36;48;5;232m\]\${CONTAINER_NAME:-docker}\[\e[0m\]\[\e[01;32m\]@\u\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ "

alias copy='wl-copy'
alias sb="source ~/.bashrc"

alias cw="cd ~/colcon_ws"
alias cs="cd ~/colcon_ws/src"
alias cb="cw && colcon build --symlink-install"
alias cbp="cw && colcon build --symlink-install --packages-select"

alias rn="ros2 node list"
alias rni="ros2 node info"

alias rt="ros2 topic list"
alias ri="ros2 topic info"
alias re="ros2 topic echo"

alias rs="ros2 service list"
alias rsi="ros2 service info"

alias ra="ros2 action list"
alias rai="ros2 action info"

alias rshow="ros2 interface show"

alias ghl='gh repo list'
alias ghc='gh repo clone'
alias ghurl='gh repo view --json url -q .url'
