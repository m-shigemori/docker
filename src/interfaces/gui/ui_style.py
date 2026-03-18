from PyQt5.QtWidgets import QPushButton, QLabel, QFrame, QScrollArea
from PyQt5.QtGui import QFont

class UIStyle:
    def __init__(self, config):
        self.config = config

    def button(self, text, btn_type="action"):
        btn = QPushButton(text)
        base_style = f"""
        QPushButton {{
            color: #ffffff;
            border: 1px solid rgba(255,255,255,0.5);
            border-radius: {self.config.BORDER_RADIUS}px;
            font-weight: bold;
            font-size: 16px;
        }}
        """
        type_styles = {
            "control": f"background: {self.config.COLORS['control_btn']}; padding: 0px 15px; height: {self.config.BUTTON_HEIGHT}px;",
            "start": f"background: {self.config.COLORS['start_btn']}; padding: 0px 15px; height: {self.config.BUTTON_HEIGHT}px;",
            "delete": f"background: {self.config.COLORS['delete_btn']}; padding: 0px 15px; height: {self.config.BUTTON_HEIGHT}px;",
            "action": f"background: {self.config.COLORS['action_btn']}; height: {self.config.BUTTON_HEIGHT}px;",
        }
        btn.setStyleSheet(base_style + f"QPushButton {{ {type_styles.get(btn_type, type_styles['action'])} }}")
        return btn

    def label(self, text, label_type="normal"):
        label = QLabel(text)
        label.setFont(QFont("Sans Serif"))
        styles = {
            "header": f"""
                color: #ffffff;
                background: {self.config.COLORS['header_bg']};
                font-weight: bold;
                font-size: 16px;
                padding: 0px;
                height: {self.config.BUTTON_HEIGHT}px;
                border-radius: {self.config.BORDER_RADIUS}px;
            """,
            "running": f"""
                color: {self.config.COLORS['running_text']};
                background: {self.config.COLORS['running_bg']};
                border: 1px solid {self.config.COLORS['running_border']};
                font-weight: bold;
                font-size: 16px;
                padding: 0px;
                height: {self.config.BUTTON_HEIGHT}px;
            """,
            "stopped": f"""
                color: {self.config.COLORS['stopped_text']};
                background: {self.config.COLORS['stopped_bg']};
                border: 1px solid {self.config.COLORS['stopped_border']};
                font-weight: bold;
                font-size: 16px;
                padding: 0px;
                height: {self.config.BUTTON_HEIGHT}px;
            """,
            "normal": "color: #ffffff; font-size: 16px; height: 42px;"
        }
        label.setStyleSheet(f"QLabel {{ {styles.get(label_type, styles['normal'])} }}")
        return label

    def frame(self):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: {self.config.COLORS['frame_bg']}; border: 1px solid rgba(255,255,255,0.5); border-radius: {self.config.BORDER_RADIUS}px; }}")
        return frame

    def scroll(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; } QScrollBar:vertical { background: rgba(0,0,0,0.3); width: 8px; border-radius: 4px; } QScrollBar::handle:vertical { background: rgba(255,255,255,0.6); min-height: 20px; border-radius: 4px; }")
        return scroll
