#!/bin/bash

# 設定とユーティリティ関数
ROS2_DISTRIBUTIONS=("humble" "galactic" "foxy")
SELECTED_ROS2_DISTRO=$1
SELECTED_ROS2_DISTRO=${SELECTED_ROS2_DISTRO//-}

check_ros2_distro() {
    local distro_to_check=$1
    if [[ ! " ${ROS2_DISTRIBUTIONS[*]} " =~ " ${distro_to_check} " ]]; then
        echo "エラー: 以下のROS2ディストリビューションから選択してください:"
        echo "       ${ROS2_DISTRIBUTIONS[*]}"
        echo "       例: bash $(basename "$0") --humble"
        exit 1
    fi
}

# メインのインストールとセットアップ処理
check_ros2_distro "${SELECTED_ROS2_DISTRO}"

echo "╔══╣ ROS2 ${SELECTED_ROS2_DISTRO} インストールとセットアップ (開始) ╠══╗"

# ROS 2ベースパッケージのインストール
sudo apt update
sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo ${UBUNTU_CODENAME}) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y ros-${SELECTED_ROS2_DISTRO}-desktop python3-colcon-common-extensions python3-rosdep2

# .bashrcにROS 2環境を設定
{
    grep -qxF "source /opt/ros/${SELECTED_ROS2_DISTRO}/setup.bash" ~/.bashrc || echo "source /opt/ros/${SELECTED_ROS2_DISTRO}/setup.bash"
    grep -qxF "export ROS_DOMAIN_ID=53" ~/.bashrc || echo "export ROS_DOMAIN_ID=53"
    grep -qxF "source /usr/share/colcon_cd/function/colcon_cd.sh" ~/.bashrc || echo "source /usr/share/colcon_cd/function/colcon_cd.sh"
    grep -qxF "export _colcon_cd_root=/opt/ros/${SELECTED_ROS2_DISTRO}/" ~/.bashrc || echo "export _colcon_cd_root=/opt/ros/${SELECTED_ROS2_DISTRO}/"
    grep -qxF "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" ~/.bashrc || echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash"
    grep -qxF "source ~/colcon_ws/install/setup.bash" ~/.bashrc || echo "source ~/colcon_ws/install/setup.bash"
} >> ~/.bashrc

# 現在のセッションのために.bashrcを読み込み
source ~/.bashrc

# Colconワークスペースを作成
rosdep update
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws
rosdep install -i --from-path src --rosdistro ${SELECTED_ROS2_DISTRO} -y
colcon build --symlink-install

# Pythonおよびシェルスクリプトの実行権限を設定 (colcon_ws/srcに配置されることを想定)
python3 -c "
import os
import subprocess

current_directory_path = os.getcwd()
up_num_to_home_dir = current_directory_path.count('/') - 2
target_dir_path = 'colcon_ws/src'
for _ in range(up_num_to_home_dir):
    target_dir_path = '../' + target_dir_path

for root, _, files in os.walk(target_dir_path):
    for file in files:
        full_path = os.path.join(root, file)
        if full_path.endswith(('.py', '.sh')):
            subprocess.run(['chmod', '755', full_path])
"

# 最終出力
echo ""
echo `printenv | grep -i ROS`
echo ""
echo "╚══╣ ROS2 ${SELECTED_ROS2_DISTRO} インストールとセットアップ (完了) ╠══╝"