from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGraphicsColorizeEffect
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize
from app.views.components import create_custom_button

class ContainerListManager:
    def __init__(self, main_layout):
        self.main_layout = main_layout
        
        self.header_row = QWidget()
        self.header_row.setContentsMargins(15, 0, 15, 0)
        self.header_layout = QHBoxLayout(self.header_row)
        self.header_layout.setContentsMargins(5, 0, 5, 0)
        self.header_layout.setSpacing(10)
        
        self.label_state = QLabel("STATE")
        self.label_name = QLabel("NAME")
        self.label_action = QLabel("ACTION")
        
        for label in [self.label_state, self.label_name, self.label_action]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        self.header_layout.addWidget(self.label_state, 2)
        self.header_layout.addWidget(self.label_name, 3)
        self.header_layout.addWidget(self.label_action, 4)
        
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
        
        self.container_rows = []

    def create_container_row(self, name, state, is_delete_mode=False):
        row_container = QWidget()
        row_layout = QVBoxLayout(row_container)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        row_frame = QFrame()
        row_frame.setObjectName("containerRow")
        row_frame.setStyleSheet("QFrame#containerRow { border: 1px solid #dcdcdc; border-radius: 8px; background: rgba(255, 255, 255, 250); }")
        
        layout = QHBoxLayout(row_frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        state_widget = QWidget()
        state_layout = QHBoxLayout(state_widget)
        state_layout.setContentsMargins(0, 0, 0, 0)
        state_layout.setSpacing(8)
        
        state_icon = QLabel()
        state_text = QLabel(state.upper())
        state_text.setFixedWidth(75)
        
        if state == "running":
            icon_path = "assets/icons/boot.svg"
            color = "#258c6d"
        else:
            icon_path = "assets/icons/down.svg"
            color = "#767676"
            
        state_icon.setProperty("path", icon_path)
        state_text.setProperty("base_color", color)
        
        icon_effect = QGraphicsColorizeEffect()
        icon_effect.setColor(QColor(color))
        state_icon.setGraphicsEffect(icon_effect)
        
        state_layout.addStretch()
        state_layout.addWidget(state_icon)
        state_layout.addWidget(state_text)
        state_layout.addStretch()
        
        name_frame = QFrame()
        name_layout = QHBoxLayout(name_frame)
        name_layout.setContentsMargins(5, 5, 5, 5)

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_layout.addWidget(name_label)
        
        action_frame = QFrame()
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(10)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_slot1 = QWidget()
        btn_slot2 = QWidget()
        
        slot1_layout = QVBoxLayout(btn_slot1)
        slot1_layout.setContentsMargins(0, 0, 0, 0)
        slot2_layout = QVBoxLayout(btn_slot2)
        slot2_layout.setContentsMargins(0, 0, 0, 0)
        
        buttons = []
        if is_delete_mode:
            btn_delete = create_custom_button("Delete", "assets/icons/note.svg")
            btn_delete.setProperty("special_color", "red")
            slot2_layout.addWidget(btn_delete)
            buttons = [btn_delete]
        elif state == "running":
            btn_exec = create_custom_button("Exec", "assets/icons/exec.svg")
            btn_stop = create_custom_button("Stop", "assets/icons/stop.svg")
            btn_stop.setProperty("special_color", "red")
            slot1_layout.addWidget(btn_exec)
            slot2_layout.addWidget(btn_stop)
            buttons = [btn_exec, btn_stop]
        else:
            btn_start = create_custom_button("Start", "assets/icons/start.svg")
            slot2_layout.addWidget(btn_start)
            buttons = [btn_start]
            
        action_layout.addWidget(btn_slot1)
        action_layout.addWidget(btn_slot2)
        
        layout.addWidget(state_widget, 2)
        layout.addWidget(name_frame, 3)
        layout.addWidget(action_frame, 4)
        
        row_layout.addWidget(row_frame)
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, row_container)
        
        self.container_rows.append({
            "row": row_container,
            "state_icon": state_icon,
            "state_text": state_text,
            "name_label": name_label,
            "buttons": buttons,
            "slots": [btn_slot1, btn_slot2]
        })

    def clear_list(self):
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.container_rows = []

    def update_styles(self, fs, icon_s, btn_h, btn_style, hover_label_style, header_label_style, list_btn_w):
        for label in [self.label_state, self.label_name, self.label_action]:
            label.setStyleSheet(header_label_style)

        for item in self.container_rows:
            base_color = item["state_text"].property("base_color")
            
            state_fs = int(fs * 0.8)
            state_icon_s = int(icon_s * 0.8)
            
            row_label_style = f"color: {base_color}; font-weight: bold; font-size: {state_fs}px; background: transparent;"
            item["state_text"].setStyleSheet(row_label_style)
            
            name_style = f"color: #4a3a35; font-weight: normal; font-size: {fs}px; background: transparent;"
            item["name_label"].setStyleSheet(name_style)
            
            icon_pix = QIcon(item["state_icon"].property("path")).pixmap(QSize(state_icon_s, state_icon_s))
            item["state_icon"].setPixmap(icon_pix)
            item["state_icon"].setFixedSize(state_icon_s, state_icon_s)
            
            for btn in item["buttons"]:
                btn_color = btn.property("special_color") or "#4a3a35"
                btn_normal_style = f"color: {btn_color}; font-weight: bold; font-size: {fs}px; background: transparent;"
                
                btn.setFixedHeight(btn_h)
                btn.setFixedWidth(int(list_btn_w))
                btn.setStyleSheet(btn_style)
                btn.set_labels(btn.icon_label, btn.text_label, btn_normal_style, hover_label_style)
                
                btn_icon_pix = QIcon(btn.icon_label.property("path")).pixmap(QSize(icon_s, icon_s))
                btn.icon_label.setPixmap(btn_icon_pix)
                btn.icon_label.setFixedSize(icon_s, icon_s)
                
            for slot in item["slots"]:
                slot.setFixedWidth(int(list_btn_w))
