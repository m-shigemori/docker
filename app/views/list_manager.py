from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGraphicsColorizeEffect
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize
from app.views.components import create_custom_button

class ContainerRow(QWidget):
    def __init__(self, name, state, is_delete_mode):
        super().__init__()
        self.name = name
        self.state = state
        self.is_delete_mode = is_delete_mode
        self.buttons = []
        
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.frame = QFrame()
        self.frame.setObjectName("containerRow")
        self.frame.setStyleSheet("QFrame#containerRow { border: 1px solid #dcdcdc; border-radius: 8px; background: rgba(255, 255, 255, 250); }")
        
        row_layout = QHBoxLayout(self.frame)
        row_layout.setContentsMargins(10, 8, 10, 8)
        row_layout.setSpacing(10)

        self.state_icon = QLabel()
        self.state_text = QLabel(self.state.upper())
        self.state_text.setFixedWidth(75)
        
        if self.state == "running":
            self.icon_path = "assets/icons/boot.svg"
            self.base_color = "#258c6d"
        else:
            self.icon_path = "assets/icons/down.svg"
            self.base_color = "#767676"
            
        self.state_icon.setProperty("path", self.icon_path)
        
        effect = QGraphicsColorizeEffect()
        effect.setColor(QColor(self.base_color))
        self.state_icon.setGraphicsEffect(effect)
        
        state_layout = QHBoxLayout()
        state_layout.setContentsMargins(0, 0, 0, 0)
        state_layout.setSpacing(8)
        state_layout.addStretch()
        state_layout.addWidget(self.state_icon)
        state_layout.addWidget(self.state_text)
        state_layout.addStretch()
        
        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(10)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_slot1 = QWidget()
        self.btn_slot2 = QWidget()
        
        slot1_layout = QVBoxLayout(self.btn_slot1)
        slot1_layout.setContentsMargins(0, 0, 0, 0)
        slot2_layout = QVBoxLayout(self.btn_slot2)
        slot2_layout.setContentsMargins(0, 0, 0, 0)
        
        if self.is_delete_mode:
            btn = create_custom_button("Delete", "assets/icons/note.svg")
            btn.setProperty("special_color", "red")
            slot2_layout.addWidget(btn)
            self.buttons.append(btn)
        elif self.state == "running":
            btn_exec = create_custom_button("Exec", "assets/icons/exec.svg")
            btn_stop = create_custom_button("Stop", "assets/icons/stop.svg")
            btn_stop.setProperty("special_color", "red")
            slot1_layout.addWidget(btn_exec)
            slot2_layout.addWidget(btn_stop)
            self.buttons.extend([btn_exec, btn_stop])
        else:
            btn_start = create_custom_button("Start", "assets/icons/start.svg")
            slot2_layout.addWidget(btn_start)
            self.buttons.append(btn_start)
            
        action_layout.addWidget(self.btn_slot1)
        action_layout.addWidget(self.btn_slot2)
        
        row_layout.addLayout(state_layout, 2)
        row_layout.addWidget(self.name_label, 3)
        row_layout.addLayout(action_layout, 4)
        
        layout.addWidget(self.frame)

    def update_styles(self, fs, icon_s, btn_h, btn_w, btn_style, hover_style):
        self.state_text.setStyleSheet(f"color: {self.base_color}; font-weight: bold; font-size: {int(fs * 0.8)}px; background: transparent;")
        self.name_label.setStyleSheet(f"color: #4a3a35; font-weight: normal; font-size: {fs}px; background: transparent;")
        
        pixmap = QIcon(self.icon_path).pixmap(QSize(int(icon_s * 0.8), int(icon_s * 0.8)))
        self.state_icon.setPixmap(pixmap)
        self.state_icon.setFixedSize(int(icon_s * 0.8), int(icon_s * 0.8))
        
        self.btn_slot1.setFixedWidth(int(btn_w))
        self.btn_slot2.setFixedWidth(int(btn_w))
        
        for btn in self.buttons:
            color = btn.property("special_color") or "#4a3a35"
            normal_style = f"color: {color}; font-weight: bold; font-size: {fs}px; background: transparent;"
            btn.update_appearance(btn_w, btn_h, icon_s, btn_style)
            btn.set_labels(normal_style, hover_style)

class ContainerListManager:
    def __init__(self, main_layout):
        self.main_layout = main_layout
        self.container_rows = []
        self._setup_ui()

    def _setup_ui(self):
        self.header_row = QWidget()
        self.header_row.setContentsMargins(15, 0, 15, 0)
        
        header_layout = QHBoxLayout(self.header_row)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(10)
        
        self.label_state = QLabel("STATE")
        self.label_name = QLabel("NAME")
        self.label_action = QLabel("ACTION")
        
        for label, stretch in [(self.label_state, 2), (self.label_name, 3), (self.label_action, 4)]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(label, stretch)
            
        self.main_layout.addWidget(self.header_row)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(15, 0, 15, 0)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()
        
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

    def clear_list(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.container_rows = []

    def create_container_row(self, name, state, is_delete_mode):
        row = ContainerRow(name, state, is_delete_mode)
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, row)
        self.container_rows.append(row)

    def update_styles(self, fs, icon_s, btn_h, btn_style, hover_style, header_style, btn_w):
        for label in [self.label_state, self.label_name, self.label_action]:
            label.setStyleSheet(header_style)
            
        for row in self.container_rows:
            row.update_styles(fs, icon_s, btn_h, btn_w, btn_style, hover_style)
