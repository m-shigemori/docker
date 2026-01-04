import os

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush

from docker_client import DockerClient
from ui_style import StyleConfig, UIStyle


class ContainerExecuter(QWidget):
    def __init__(self):
        super().__init__()

        self.client = DockerClient()
        self.config = StyleConfig()
        self.ui = UIStyle(self.config)
        self.containers = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ContainerExecuter")
        self.setFixedSize(*self.config.WINDOW_SIZE)
        self.move(0, 0)

        self._setup_background()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.refresh_gui()
        self.show()

    def _setup_background(self):
        image_path = os.path.join(
            os.path.dirname(__file__),
            "img",
            "kotone.jpg",
        )

        if not os.path.exists(image_path):
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        w, h = self.config.WINDOW_SIZE
        scaled = pixmap.scaled(
            w,
            h,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )

        x = (scaled.width() - w) // 2
        y = (scaled.height() - h) // 2
        final = scaled.copy(x, y, w, h)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(final))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def refresh_gui(self):
        self.containers = self.client.list_containers()
        self._update_gui()

    def _update_gui(self):
        self._clear_layout(self.main_layout)

        frame = self.ui.frame()
        frame.setFixedWidth(self.config.FRAME_WIDTH)
        frame.setMaximumHeight(
            int(self.height() * self.config.FRAME_MAX_HEIGHT_RATIO)
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)

        layout.addLayout(self._create_control_section())
        layout.addSpacing(15)
        layout.addLayout(self._create_header_section())

        layout.addSpacing(8)
        layout.addWidget(self._create_divider())
        layout.addSpacing(8)

        layout.addWidget(self._create_scroll_section())

        self.main_layout.addWidget(frame)

    def _create_control_section(self):
        layout = QHBoxLayout()

        refresh_btn = self.ui.button("Refresh", "control")
        refresh_btn.clicked.connect(self.refresh_gui)

        close_btn = self.ui.button("Close", "control")
        close_btn.clicked.connect(self.close)

        layout.addWidget(refresh_btn)
        layout.addWidget(close_btn)
        layout.addStretch()

        return layout

    def _create_header_section(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        headers = [
            ("State", "state"),
            ("Name", "name"),
            ("Control", "control"),
        ]

        for text, key in headers:
            label = self.ui.label(text, "header")
            label.setFixedHeight(self.config.BUTTON_HEIGHT)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            layout.setStretchFactor(label, self.config.COLUMN_STRETCH[key])

        return layout

    def _create_scroll_section(self):
        scroll = self.ui.scroll()

        content = QWidget()
        content.setStyleSheet("background: transparent;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        for container in self.containers:
            content_layout.addLayout(
                self._create_container_row(container)
            )

        content_layout.addStretch()
        scroll.setWidget(content)

        return scroll

    def _create_container_row(self, container):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        state_label = self.ui.label(
            "Running" if container.is_running else "Stopped",
            "running" if container.is_running else "stopped",
        )
        state_label.setAlignment(Qt.AlignCenter)
        state_label.setFixedHeight(self.config.BUTTON_HEIGHT)
        state_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        name_label = self.ui.label(container.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFixedHeight(self.config.BUTTON_HEIGHT)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(state_label)
        layout.addWidget(name_label)

        action_widget = self._create_action_buttons(container)
        action_widget.setFixedHeight(self.config.BUTTON_HEIGHT)
        action_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(action_widget)

        layout.setStretch(0, self.config.COLUMN_STRETCH["state"])
        layout.setStretch(1, self.config.COLUMN_STRETCH["name"])
        layout.setStretch(2, self.config.COLUMN_STRETCH["control"])

        return layout

    def _create_action_buttons(self, container):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(widget)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        if container.is_running:
            actions = [
                ("■", "stop"),
                ("⚡", "exec"),
            ]

            for text, action in actions:
                btn = self.ui.button(text)
                btn.setFixedHeight(self.config.BUTTON_HEIGHT)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.clicked.connect(
                    lambda _, a=action, c=container.id:
                    self._handle_action(a, c)
                )
                layout.addWidget(btn)
        else:
            btn = self.ui.button("▶ Start", "start")
            btn.setFixedHeight(self.config.BUTTON_HEIGHT)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(
                lambda: self._handle_action(
                    "start",
                    container.id,
                )
            )
            layout.addWidget(btn)

        return widget

    def _handle_action(self, action, container_id):
        actions = {
            "start": self.client.start,
            "stop": self.client.stop,
            "exec": self.client.exec_shell,
        }

        if action in actions:
            actions[action](container_id)
            self.refresh_gui()

    def _create_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(
            "background-color: rgba(255,255,255,0.5); border: none; height: 1px;"
        )
        return line

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())


if __name__ == "__main__":
    app = QApplication([])
    ce = ContainerExecuter()
    app.exec_()