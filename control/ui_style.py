from PyQt5.QtWidgets import QPushButton, QLabel, QFrame, QScrollArea
from PyQt5.QtGui import QFont


class StyleConfig:
    BORDER_RADIUS = 8
    BUTTON_HEIGHT = 42
    CONTROL_BUTTON_WIDTH = 90
    ACTION_BUTTON_WIDTH = 36

    WINDOW_SIZE = (960, 540)
    FRAME_WIDTH = 440
    FRAME_MAX_HEIGHT_RATIO = 0.9

    COLUMN_STRETCH = {
        "state": 3,
        "name": 5,
        "control": 5,
    }

    COLORS = {
        "frame_bg": "rgba(0,0,0,0.85)",
        "frame_border": "rgba(255,255,255,0.3)",
        "control_btn": "rgba(60,60,60,0.8)",
        "start_btn": "rgba(46,204,113,0.8)",
        "action_btn": "rgba(52,152,219,0.8)",
        "running_text": "#2ecc71",
        "running_bg": "rgba(46,204,113,0.1)",
        "running_border": "rgba(46,204,113,0.3)",
        "stopped_text": "#e74c3c",
        "stopped_bg": "rgba(231,76,60,0.1)",
        "stopped_border": "rgba(231,76,60,0.3)",
        "header_text": "#ffffff",
        "header_bg": "rgba(255,255,255,0.1)",
    }


class UIStyle:
    def __init__(self, config: StyleConfig):
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
            "control": f"""
                background: {self.config.COLORS['control_btn']};
                padding: 0px 15px;
                height: {self.config.BUTTON_HEIGHT}px;
            """,
            "start": f"""
                background: {self.config.COLORS['start_btn']};
                padding: 0px 15px;
                height: {self.config.BUTTON_HEIGHT}px;
            """,
            "action": f"""
                background: {self.config.COLORS['action_btn']};
                height: {self.config.BUTTON_HEIGHT}px;
            """,
        }

        btn.setStyleSheet(
            base_style
            + f"QPushButton {{ {type_styles.get(btn_type, type_styles['action'])} }}"
        )
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
            "normal": f"color: #ffffff; font-size: 16px; height: {self.config.BUTTON_HEIGHT}px;",
        }

        label.setStyleSheet(
            f"QLabel {{ {styles.get(label_type, styles['normal'])} }}"
        )
        return label

    def frame(self):
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {self.config.COLORS['frame_bg']};
                border: 1px solid rgba(255,255,255,0.5);
                border-radius: {self.config.BORDER_RADIUS}px;
            }}
            """
        )
        return frame

    def scroll(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.3);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.6);
                min-height: 20px;
                border-radius: 4px;
            }
            """
        )
        return scroll