from PyQt6.QtWidgets import QPushButton, QGraphicsColorizeEffect, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize

class HoverButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.icon_label = QLabel()
        self.icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.icon_label.setProperty("path", icon_path)
        
        self.text_label = QLabel(text)
        self.text_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        self.icon_effect = QGraphicsColorizeEffect()
        self.icon_effect.setColor(QColor("white"))
        self.icon_effect.setEnabled(False)
        self.icon_label.setGraphicsEffect(self.icon_effect)
        
        self.normal_style = ""
        self.hover_style = ""

    def set_labels(self, normal_style, hover_style):
        self.normal_style = normal_style
        self.hover_style = hover_style
        self._apply_current_style()

    def _apply_current_style(self):
        is_hover = self.underMouse()
        self.icon_effect.setEnabled(is_hover)
        
        if self.text_label:
            self.text_label.setStyleSheet(self.hover_style if is_hover else self.normal_style)

    def enterEvent(self, event):
        super().enterEvent(event)

        self.icon_effect.setEnabled(True)
        if self.text_label:
            self.text_label.setStyleSheet(self.hover_style)

    def leaveEvent(self, event):
        super().leaveEvent(event)

        self.icon_effect.setEnabled(False)
        if self.text_label:
            self.text_label.setStyleSheet(self.normal_style)

    def update_appearance(self, w, h, icon_s, btn_style):
        self.setFixedSize(int(w), int(h))
        self.setStyleSheet(btn_style)
        
        pixmap = QIcon(self.icon_label.property("path")).pixmap(QSize(icon_s, icon_s))
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(icon_s, icon_s)

    def set_text(self, text):
        self.text_label.setText(text)
        self._apply_current_style()

def create_custom_button(text, icon_path):
    return HoverButton(text, icon_path)
