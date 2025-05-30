#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush

class ContainerExecuter(QWidget):
    def __init__(self):
        super().__init__()
        self.running_containers_info = []
        self.containers_info = []
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ContainerExecuter")
        # ウィンドウサイズを800x600に固定
        self.setFixedSize(800, 600)

        # 背景画像の設定
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, 'img', 'mika.jpg')

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # ウィンドウサイズに合わせて画像をスケーリング
                scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                palette = self.palette()
                palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
                self.setPalette(palette)
                self.setAutoFillBackground(True)
            else:
                print(f"Warning: Could not load image from {image_path}")
        else:
            print(f"Warning: Image file not found at {image_path}")

        self.update_gui_content()
        self.show()

    def update_gui_content(self):
        self.clear_layout(self.main_layout)

        self.get_containers_info(is_running=False)
        self.get_containers_info(is_running=True)

        # 上部のコントロールボタン (Refresh, Close)
        control_buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_gui)
        control_buttons_layout.addWidget(refresh_button)

        close_button = QPushButton("close")
        close_button.clicked.connect(self.close_gui)
        control_buttons_layout.addWidget(close_button)
        control_buttons_layout.addStretch(1) # 右に寄せる
        self.main_layout.addLayout(control_buttons_layout)

        # ヘッダー行の追加
        header_layout = QHBoxLayout()
        # "state"
        state_header = QLabel("state")
        state_header.setStyleSheet("font-size: 15px; color: black; background-color: rgba(255, 255, 255, 100); padding: 5px;")
        state_header.setFixedWidth(100) # 幅を固定
        state_header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(state_header)

        # "name"
        name_header = QLabel("name")
        name_header.setStyleSheet("font-size: 15px; color: black; background-color: rgba(255, 255, 255, 100); padding: 5px;")
        name_header.setFixedWidth(150) # 幅を固定
        name_header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(name_header)

        # "control"
        control_header = QLabel("control")
        control_header.setStyleSheet("font-size: 15px; color: black; background-color: rgba(255, 255, 255, 100); padding: 5px;")
        control_header.setFixedWidth(250) # 幅を固定
        control_header.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(control_header)
        header_layout.addStretch(1) # 右に寄せる
        self.main_layout.addLayout(header_layout)


        for container_info in self.containers_info:
            container_id = container_info[0]
            container_name = container_info[-1].replace(" ", "")

            row_layout = QHBoxLayout()

            is_running = any(container_id == rc_info[0] for rc_info in self.running_containers_info)

            # State Label
            state_label = QLabel("Running" if is_running else "Stopped")
            state_label.setStyleSheet(f"font-size: 15px; color: {'green' if is_running else 'red'}; background-color: rgba(255, 255, 255, 150); padding: 5px;")
            state_label.setFixedWidth(100) # 幅を固定
            state_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            row_layout.addWidget(state_label)

            # Container Name Label
            container_name_label = QLabel(container_name)
            container_name_label.setStyleSheet("font-size: 15px; color: black; background-color: rgba(255, 255, 255, 150); padding: 5px;")
            container_name_label.setFixedWidth(150) # 幅を固定
            container_name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            row_layout.addWidget(container_name_label)

            # Control Buttons
            if is_running:
                restart_button = QPushButton("restart")
                restart_button.clicked.connect(self.button_clicked_callback("restart", container_id))
                row_layout.addWidget(restart_button)
                restart_button.setFixedWidth(70)

                stop_button = QPushButton("stop")
                stop_button.clicked.connect(self.button_clicked_callback("stop", container_id))
                row_layout.addWidget(stop_button)
                stop_button.setFixedWidth(70)

                exec_button = QPushButton("exec")
                exec_button.clicked.connect(self.button_clicked_callback("exec", container_id))
                row_layout.addWidget(exec_button)
                exec_button.setFixedWidth(70)
            else:
                start_button = QPushButton("start")
                start_button.clicked.connect(self.button_clicked_callback("start", container_id))
                row_layout.addWidget(start_button)
                start_button.setFixedWidth(70)
                # startボタンの右にスペースを確保
                row_layout.addStretch(1) # 残りのスペースを埋める

            row_layout.addStretch(1) # 右に寄せる
            self.main_layout.addLayout(row_layout)

        self.main_layout.addStretch(1) # 残りのスペースを埋める

    def add_button(self, layout: QHBoxLayout, operation: str, container_id: str):
        button = QPushButton(operation)
        button.clicked.connect(self.button_clicked_callback(operation, container_id))
        layout.addWidget(button)

    def button_clicked_callback(self, operation: str, container_id: str):
        def inner():
            cmd = ""
            if operation == "exec":
                print(f"[{container_id}] container has been executed.")
                cmd = f"gnome-terminal -- bash -c 'docker exec -it --user sobits {container_id} /bin/bash; bash'"
            elif operation == "start":
                print(f"[{container_id}] container has been started.")
                cmd = f"docker start {container_id} "
            elif operation == "restart":
                print(f"[{container_id}] container has been restarted.")
                cmd = f"docker restart {container_id} "
            elif operation == "stop":
                print(f"[{container_id}] container has been stopped.")
                cmd = f"docker stop {container_id} "

            if cmd:
                try:
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    QMessageBox.critical(self, "Error", f"Command failed: {e}")
            self.refresh_gui()
        return inner

    def close_gui(self):
        print("[close] button has been clicked.")
        self.close()

    def refresh_gui(self):
        print("[refresh] button has been clicked.")
        self.running_containers_info = []
        self.containers_info = []
        self.update_gui_content()

    def clear_layout(self, layout: QLayout):
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def get_containers_info(self, is_running=False):
        cmd = "docker ps" if is_running else "docker ps -a"
        res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, text=True, check=True)
        containers_info_raw = res.stdout.split("\n")

        for i, container_info_line in enumerate(containers_info_raw):
            if 0 < i < len(containers_info_raw) - 1:
                container_info_parts = re.split(r'\s{2,}', container_info_line.strip())
                container_info = [x for x in container_info_parts if x]
                if is_running:
                    self.running_containers_info.append(container_info)
                else:
                    self.containers_info.append(container_info)

if __name__ == "__main__":
    app = QApplication([])
    ce = ContainerExecuter()
    app.exec_()