import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QDesktopWidget, QSizePolicy, QLabel, QGraphicsBlurEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

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

        self.bg_label = None
        self.img_label = None
        self.left_panel = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ContainerExecuter")
        self.setMinimumSize(*self.config.MIN_WINDOW_SIZE)
        self.resize(*self.config.MIN_WINDOW_SIZE)
        self._center_window()

        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(False)

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.bg_label.setGraphicsEffect(blur_effect)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(self.config.SIDE_MARGIN, 0, 0, 0)
        self.main_layout.setSpacing(self.config.SIDE_MARGIN)

        self.refresh_gui()
        self.show()

    def _center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _update_layout_sizes(self):
        if not os.path.exists(self.config.IMAGE_PATH):
            return

        pixmap = QPixmap(self.config.IMAGE_PATH)

        self.bg_label.setPixmap(pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()

        h = self.height()
        scaled = pixmap.scaledToHeight(h, Qt.SmoothTransformation)
        img_w = scaled.width()

        if self.img_label:
            self.img_label.setPixmap(scaled)
            self.img_label.setFixedWidth(img_w)

        if self.left_panel:
            panel_w = self.width() - img_w - (self.config.SIDE_MARGIN * 2)
            self.left_panel.setFixedWidth(panel_w)
            self.left_panel.setFixedHeight(self.height() - 40)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_layout_sizes()

    def refresh_gui(self):
        self._clear_layout(self.main_layout)
        containers = self.client.list_containers()

        self.left_panel = self.ui.frame()
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(15, 15, 15, 15)
        panel_layout.setSpacing(0)

        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(10)
        refresh_btn = self.ui.button("Refresh", "control")
        refresh_btn.clicked.connect(self.refresh_gui)
        close_btn = self.ui.button("Close", "control")
        close_btn.clicked.connect(self.close)
        ctrl_layout.addWidget(refresh_btn)
        ctrl_layout.addWidget(close_btn)
        ctrl_layout.addStretch()
        panel_layout.addLayout(ctrl_layout)

        panel_layout.addSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        for text, key in [("State", "state"), ("Name", "name"), ("Control", "control")]:
            label = self.ui.label(text, "header")
            label.setFixedHeight(self.config.BUTTON_HEIGHT)
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
            header_layout.setStretchFactor(label, self.config.COLUMN_STRETCH[key])
        panel_layout.addLayout(header_layout)

        panel_layout.addSpacing(8)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: rgba(255,255,255,0.3); border: none; height: 1px;")
        panel_layout.addWidget(line)

        panel_layout.addSpacing(8)

        scroll = self.ui.scroll()
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        for c in containers:
            content_layout.addWidget(ContainerRow(c, self.ui, self.config, self._handle_action))

        content_layout.addStretch()
        scroll.setWidget(scroll_content)
        panel_layout.addWidget(scroll)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.img_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.img_label.setStyleSheet("background: transparent;")

        self.main_layout.addWidget(self.left_panel, alignment=Qt.AlignVCenter)
        self.main_layout.addWidget(self.img_label)

        self._update_layout_sizes()

    def _handle_action(self, action, container_id):
        actions = {"start": self.client.start, "stop": self.client.stop, "exec": self.client.exec_shell}
        if action in actions:
            actions[action](container_id)
            self.refresh_gui()

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