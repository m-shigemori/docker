from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize
from app.views.components import create_custom_button

class ControlPanelManager:
    def __init__(self, master):
        self.master = master
        self.frame = QFrame(self.master)
        
        self.main_layout = QVBoxLayout(self.frame)
        self.main_layout.setContentsMargins(0, 15, 0, 15)
        self.main_layout.setSpacing(15)
        
        self.button_row = QWidget()
        self.button_row.setContentsMargins(15, 0, 15, 0)
        
        self.row_layout = QHBoxLayout(self.button_row)
        self.row_layout.setContentsMargins(5, 5, 5, 10)
        self.row_layout.setSpacing(10)
        
        self.btn_refresh = create_custom_button("Refresh", "assets/icons/reflesh.svg")
        self.btn_toggle = create_custom_button("Operation", "assets/icons/operation.svg")
        self.btn_close = create_custom_button("Close", "assets/icons/close.svg")
        
        self.row_layout.addWidget(self.btn_refresh)
        self.row_layout.addWidget(self.btn_toggle)
        self.row_layout.addStretch()
        self.row_layout.addWidget(self.btn_close)
        
        self.main_layout.addWidget(self.button_row)
        
        self.separator = QFrame()
        self.separator.setFixedHeight(1)
        self.separator.setStyleSheet("background-color: #dcdcdc; border: none;")
        
        line_shadow = QGraphicsDropShadowEffect(self.separator)
        line_shadow.setBlurRadius(4)
        line_shadow.setXOffset(0)
        line_shadow.setYOffset(1)
        line_shadow.setColor(QColor(0, 0, 0, 20))
        self.separator.setGraphicsEffect(line_shadow)
        
        self.main_layout.addWidget(self.separator)

    def toggle_mode(self, is_delete_mode):
        if is_delete_mode:
            self.btn_toggle.set_text("Delete")
            self.btn_toggle.icon_label.setProperty("path", "assets/icons/bin.svg")
        else:
            self.btn_toggle.set_text("Operation")
            self.btn_toggle.icon_label.setProperty("path", "assets/icons/operation.svg")

    def update_styles(self, btn_w, btn_h, icon_s, btn_style, normal_style, hover_style):
        for btn in [self.btn_refresh, self.btn_toggle, self.btn_close]:
            btn.update_appearance(btn_w, btn_h, icon_s, btn_style)
            btn.set_labels(normal_style, hover_style)
