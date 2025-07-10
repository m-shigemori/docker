#!/bin/bash

# 設定とユーティリティ関数
ROS_VERall=("ros2")
SELECTED_ROS_VER=$1
SELECTED_ROS_VER=${SELECTED_ROS_VER//-}

check_ros_ver() {
    local ver_to_check=$1
    if [[ ! " ${ROS_VERall[*]} " =~ " ${ver_to_check} " ]]; then
        echo "エラー: 以下のROSバージョンから選択してください:"
        echo "       ${ROS_VERall[*]}"
        echo "       例: bash $(basename "$0") --ros2"
        exit 1
    fi
}

# メインのセットアップ処理
check_ros_ver "${SELECTED_ROS_VER}"

echo "╔══╣ ROS2環境エイリアスセットアップ (開始) ╠══╗"

# .bash_aliasesファイルを作成または追記
ALIAS_FILE="/home/${USER}/.bash_aliases"
touch "${ALIAS_FILE}"

# pip
echo "# pip" >> "${ALIAS_FILE}"
echo "alias pip='python -m pip'" >> "${ALIAS_FILE}"
echo "alias pip3='python3 -m pip'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

# ls
echo "# ls" >> "${ALIAS_FILE}"
echo "alias ls='ls --color=auto'" >> "${ALIAS_FILE}"
echo "alias ll='ls -alF'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

# cd
echo "# cd" >> "${ALIAS_FILE}"
echo "alias roscd='cd ~/colcon_ws/src'" >> "${ALIAS_FILE}"
echo "alias ..='cd ..'" >> "${ALIAS_FILE}"
echo "alias ...='cd ../..'" >> "${ALIAS_FILE}"
echo "alias ....='cd ../../..'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

# cp,mv,rm
echo "# cp,mv,rm" >> "${ALIAS_FILE}"
echo "alias cp='cp -i'" >> "${ALIAS_FILE}"
echo "alias mv='mv -i'" >> "${ALIAS_FILE}"
echo "alias rm='rm -i'" >> "${ALIAS_FILE}"
echo "" >> "${ALIAS_FILE}"

# 共通の環境変数設定
echo "export PYTHONDONTWRITEBYTECODE=1" >> "${ALIAS_FILE}"
echo "export PS1='\[\e[1;33;40m\]\$CONTAINER_NAME\[\e[0m\] \${debian_chroot:+(\$debian_chroot)}\[\033[01;32m\]\u@\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> "${ALIAS_FILE}"
echo "export EDITOR='nano'" >> "${ALIAS_FILE}"

echo "╚══╣ ROS2環境エイリアスセットアップ (完了) ╠══╝"