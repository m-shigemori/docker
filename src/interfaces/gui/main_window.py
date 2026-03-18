from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QDesktopWidget, QSizePolicy, QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from .ui_style import UIStyle
from .ui_manager import UIManager
from .widgets import ContainerRow

class MainWindow(QWidget):
    def __init__(self, container_service, config):
        super().__init__()
        self.container_service = container_service
        self.config = config
        self.ui = UIStyle(self.config)
        self.ui_manager = UIManager(self, self.config)

        self.img_label = None
        self.left_panel = None
        self.delete_mode = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ContainerExecuter")
        self.setMinimumSize(*self.config.MIN_WINDOW_SIZE)
        self.resize(*self.config.MIN_WINDOW_SIZE)

        self._set_initial_position()

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(self.config.SIDE_MARGIN, 0, 0, 0)
        self.main_layout.setSpacing(self.config.SIDE_MARGIN)

        self.refresh_gui()
        self.show()

    def _set_initial_position(self):
        desktop = QDesktopWidget()
        cursor_pos = QCursor.pos()
        screen_idx = desktop.screenNumber(cursor_pos)
        geo = desktop.availableGeometry(screen_idx)
        self.move(geo.topLeft())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.img_label:
            self.ui_manager.update_background(self.img_label, self.left_panel)

    def trigger_refresh(self):
        self.config.refresh_image_path()
        self.ui_manager.fade_refresh(self.refresh_gui)

    def toggle_delete_mode(self):
        self.delete_mode = not self.delete_mode
        self.refresh_gui()

    def refresh_gui(self):
        self._clear_layout(self.main_layout)

        containers = self.container_service.list_containers()

        self.left_panel = self.ui.frame()
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(15, 15, 15, 15)
        panel_layout.setSpacing(0)

        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(10)
        
        refresh_btn = self.ui.button("Refresh", "control")
        refresh_btn.clicked.connect(self.trigger_refresh)
        
        mode_btn_text = "Mode: Standard" if not self.delete_mode else "Mode: Edit"
        mode_btn = self.ui.button(mode_btn_text, "control" if not self.delete_mode else "delete")
        mode_btn.clicked.connect(self.toggle_delete_mode)

        close_btn = self.ui.button("Close", "control")
        close_btn.clicked.connect(self.close)
        
        ctrl_layout.addWidget(refresh_btn)
        ctrl_layout.addWidget(mode_btn)
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
            content_layout.addWidget(ContainerRow(c, self.ui, self.config, self._handle_action, self.delete_mode))

        content_layout.addStretch()
        scroll.setWidget(scroll_content)
        panel_layout.addWidget(scroll)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.img_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.img_label.setStyleSheet("background: transparent;")

        self.main_layout.addWidget(self.left_panel, alignment=Qt.AlignVCenter)
        self.main_layout.addWidget(self.img_label)

        self.ui_manager.update_background(self.img_label, self.left_panel)

    def _handle_action(self, action, data):
        if action == "start":
            self.container_service.start_container(data)
            self.trigger_refresh()
        elif action == "stop":
            self.container_service.stop_container(data)
            self.refresh_gui()
        elif action == "exec":
            self.container_service.open_container_shell(data)
        elif action == "delete_all":
            reply = QMessageBox.question(self, 'Confirmation', 
                                       f"Are you sure you want to delete container '{data.name}' and its image '{data.image}'?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.container_service.remove_container(data.id)
                    try:
                        self.container_service.remove_image(data.image)
                        QMessageBox.information(self, "Success", f"Container and Image '{data.image}' removed.")
                    except Exception as img_e:
                        QMessageBox.warning(self, "Warning", f"Container removed, but Image '{data.image}' could not be removed (might be in use by other containers).")
                    
                    self.refresh_gui()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
