import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QDesktopWidget, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush

from scripts.docker_client import DockerClient
from scripts.ui_style import UIStyle
from scripts.config import StyleConfig
from scripts.widgets import ContainerRow

class ContainerExecuter(QWidget):
    def __init__(self):
        super().__init__()
        self.client = DockerClient()
        self.config = StyleConfig()
        self.ui = UIStyle(self.config)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ContainerExecuter")
        self.setFixedSize(*self.config.WINDOW_SIZE)
        self._center_window()
        self._setup_background()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.refresh_gui()
        self.show()

    def _center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _setup_background(self):
        if not os.path.exists(self.config.IMAGE_PATH):
            return
        pixmap = QPixmap(self.config.IMAGE_PATH)
        w, h = self.config.WINDOW_SIZE
        scaled = pixmap.scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        final = scaled.copy((scaled.width() - w) // 2, (scaled.height() - h) // 2, w, h)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(final))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def refresh_gui(self):
        self._clear_layout(self.main_layout)
        containers = self.client.list_containers()

        frame = self.ui.frame()
        frame.setFixedWidth(self.config.FRAME_WIDTH)
        frame.setMaximumHeight(int(self.height() * self.config.FRAME_MAX_HEIGHT_RATIO))

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)

        ctrl_layout = QHBoxLayout()
        refresh_btn = self.ui.button("Refresh", "control")
        refresh_btn.clicked.connect(self.refresh_gui)
        close_btn = self.ui.button("Close", "control")
        close_btn.clicked.connect(self.close)
        ctrl_layout.addWidget(refresh_btn)
        ctrl_layout.addWidget(close_btn)
        ctrl_layout.addStretch()
        layout.addLayout(ctrl_layout)
        layout.addSpacing(15)

        header_layout = QHBoxLayout()
        for text, key in [("State", "state"), ("Name", "name"), ("Control", "control")]:
            label = self.ui.label(text, "header")
            label.setFixedHeight(self.config.BUTTON_HEIGHT)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
            header_layout.setStretchFactor(label, self.config.COLUMN_STRETCH[key])
        layout.addLayout(header_layout)
        layout.addSpacing(8)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: rgba(255,255,255,0.5); border: none; height: 1px;")
        layout.addWidget(line)
        layout.addSpacing(8)

        scroll = self.ui.scroll()
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)
        for c in containers:
            content_layout.addWidget(ContainerRow(c, self.ui, self.config, self._handle_action))
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.main_layout.addWidget(frame)

    def _handle_action(self, action, container_id):
        actions = {"start": self.client.start, "stop": self.client.stop, "exec": self.client.exec_shell}
        if action in actions:
            actions[action](container_id)
            self.refresh_gui()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.layout(): self._clear_layout(item.layout())

if __name__ == "__main__":
    app = QApplication([])
    ce = ContainerExecuter()
    app.exec_()