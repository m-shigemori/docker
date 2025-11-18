import os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont

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
        self.setFixedSize(800, 600)

        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, 'img', 'mika.jpg')

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                palette = self.palette()
                palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
                self.setPalette(palette)
                self.setAutoFillBackground(True)
            else:
                print(f"Warning: Could not load image from {image_path}")
        else:
            print(f"Warning: Image file not found at {image_path}")

        self.main_layout.setContentsMargins(20, 20, 400, 300)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.update_gui_content()
        self.move(0, 0)
        self.show()

    def create_styled_frame(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        return frame

    def create_styled_button(self, text, button_type="normal"):
        button = QPushButton(text)

        if button_type == "control":
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(70, 70, 70, 0.9);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 6px;
                    padding: 4px 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(90, 90, 90, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.5);
                }
                QPushButton:pressed {
                    background-color: rgba(50, 50, 50, 0.9);
                }
            """)
        elif button_type == "start":
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(34, 139, 34, 0.9);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(50, 160, 50, 0.9);
                }
                QPushButton:pressed {
                    background-color: rgba(20, 120, 20, 0.9);
                }
            """)
        elif button_type == "stop":
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(220, 20, 60, 0.9);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(240, 40, 80, 0.9);
                }
                QPushButton:pressed {
                    background-color: rgba(200, 10, 50, 0.9);
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(70, 130, 180, 0.9);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(90, 150, 200, 0.9);
                }
                QPushButton:pressed {
                    background-color: rgba(50, 110, 160, 0.9);
                }
            """)

        return button

    def create_styled_label(self, text, label_type="normal"):
        label = QLabel(text)
        font = QFont()
        font.setFamily("Arial")

        if label_type == "header":
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: rgba(0, 0, 0, 0.7);
                    border: 1px solid rgba(255, 255, 255, 0.4);
                    border-radius: 4px;
                    padding: 6px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """)
            font.setBold(True)
            font.setPointSize(11)
        elif label_type == "running":
            label.setStyleSheet("""
                QLabel {
                    color: #00FF00;
                    background-color: rgba(0, 50, 0, 0.8);
                    border: 1px solid rgba(0, 255, 0, 0.3);
                    border-radius: 4px;
                    padding: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            font.setBold(True)
            font.setPointSize(10)
        elif label_type == "stopped":
            label.setStyleSheet("""
                QLabel {
                    color: #FF6B6B;
                    background-color: rgba(50, 0, 0, 0.8);
                    border: 1px solid rgba(255, 0, 0, 0.3);
                    border-radius: 4px;
                    padding: 4px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            font.setBold(True)
            font.setPointSize(10)
        else:
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: rgba(40, 40, 40, 0.8);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                    padding: 4px;
                    font-size: 12px;
                }
            """)
            font.setPointSize(10)

        label.setFont(font)
        return label

    def update_gui_content(self):
        self.clear_layout(self.main_layout)

        self.get_containers_info(is_running=False)
        self.get_containers_info(is_running=True)

        main_frame = self.create_styled_frame()
        main_frame_layout = QVBoxLayout(main_frame)
        main_frame.setFixedWidth(390)
        main_frame.setMinimumHeight(320)

        control_buttons_layout = QHBoxLayout()
        refresh_button = self.create_styled_button("Refresh", "control")
        refresh_button.clicked.connect(self.refresh_gui)
        control_buttons_layout.addWidget(refresh_button)

        close_button = self.create_styled_button("Close", "control")
        close_button.clicked.connect(self.close_gui)
        control_buttons_layout.addWidget(close_button)

        control_buttons_layout.addStretch(1)
        main_frame_layout.addLayout(control_buttons_layout)

        main_frame_layout.addSpacing(10)

        header_layout = QHBoxLayout()

        state_header = self.create_styled_label("State", "header")
        state_header.setFixedWidth(80)
        state_header.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(state_header)

        name_header = self.create_styled_label("Name", "header")
        name_header.setFixedWidth(100)
        name_header.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(name_header)

        control_header = self.create_styled_label("Control", "header")
        control_header.setFixedWidth(160)
        control_header.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(control_header)

        main_frame_layout.addLayout(header_layout)

        for container_info in self.containers_info:
            container_id = container_info[0]
            container_name = container_info[-1].replace(" ", "")

            row_layout = QHBoxLayout()
            is_running = any(container_id == rc_info[0] for rc_info in self.running_containers_info)

            state_label = self.create_styled_label(
                "Running" if is_running else "Stopped",
                "running" if is_running else "stopped"
            )
            state_label.setFixedWidth(80)
            state_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(state_label)

            container_name_label = self.create_styled_label(container_name)
            container_name_label.setFixedWidth(100)
            container_name_label.setAlignment(Qt.AlignCenter)
            row_layout.addWidget(container_name_label)

            control_layout = QHBoxLayout()
            control_layout.setSpacing(4)
            control_layout.setContentsMargins(0, 0, 0, 0)

            if is_running:
                spacer_widget = QWidget()
                spacer_widget.setFixedWidth(51)
                control_layout.addWidget(spacer_widget)

                restart_button = self.create_styled_button("↻")
                restart_button.clicked.connect(self.button_clicked_callback("restart", container_id))
                restart_button.setFixedSize(32, 24)
                control_layout.addWidget(restart_button)

                stop_button = self.create_styled_button("■", "stop")
                stop_button.clicked.connect(self.button_clicked_callback("stop", container_id))
                stop_button.setFixedSize(32, 24)
                control_layout.addWidget(stop_button)

                exec_button = self.create_styled_button("⚡")
                exec_button.clicked.connect(self.button_clicked_callback("exec", container_id))
                exec_button.setFixedSize(32, 24)
                control_layout.addWidget(exec_button)
            else:
                start_button = self.create_styled_button("▶", "start")
                start_button.clicked.connect(self.button_clicked_callback("start", container_id))
                start_button.setFixedSize(50, 24)
                control_layout.addWidget(start_button)

            control_layout.addStretch(1)

            control_widget = QWidget()
            control_widget.setLayout(control_layout)
            control_widget.setFixedWidth(160)
            row_layout.addWidget(control_widget)

            main_frame_layout.addLayout(row_layout)
            main_frame_layout.addSpacing(4)

        main_frame_layout.addStretch(1)
        self.main_layout.addWidget(main_frame)

    def add_button(self, layout: QHBoxLayout, operation: str, container_id: str):
        button = QPushButton(operation)
        button.clicked.connect(self.button_clicked_callback(operation, container_id))
        layout.addWidget(button)

    def button_clicked_callback(self, operation: str, container_id: str):
        def inner():
            cmd = ""
            if operation == "exec":
                print(f"[{container_id}] container has been executed.")
                cmd = f"gnome-terminal -- bash -c 'docker exec -it {container_id} /bin/bash; bash'"
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