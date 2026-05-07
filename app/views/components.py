from PyQt6.QtWidgets import QPushButton, QGraphicsColorizeEffect, QLabel, QHBoxLayout
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize

class HoverButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.icon_label = None
        self.text_label = None
        
        self.icon_effect = QGraphicsColorizeEffect()
        self.icon_effect.setColor(QColor("white"))
        self.icon_effect.setEnabled(False)
        
        self.normal_style = ""
        self.hover_style = ""

    def set_labels(self, icon_label, text_label, normal_style="", hover_style=""):
        self.icon_label = icon_label
        self.text_label = text_label
        
        if normal_style: self.normal_style = normal_style
        if hover_style: self.hover_style = hover_style
        
        self.icon_label.setGraphicsEffect(self.icon_effect)
        
        if self.text_label and self.normal_style:
            if self.underMouse() and self.hover_style:
                self.text_label.setStyleSheet(self.hover_style)
                self.icon_effect.setEnabled(True)
            else:
                self.text_label.setStyleSheet(self.normal_style)
                self.icon_effect.setEnabled(False)

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

    def set_text(self, text):
        if self.text_label:
            self.text_label.setText(text)
            
            if self.underMouse():
                self.text_label.setStyleSheet(self.hover_style)
                self.icon_effect.setEnabled(True)
            else:
                self.text_label.setStyleSheet(self.normal_style)
                self.icon_effect.setEnabled(False)

def create_custom_button(text, icon_path):
    btn = HoverButton()
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    
    layout = QHBoxLayout(btn)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    icon_label = QLabel()
    icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    icon_label.setProperty("path", icon_path)
    
    text_label = QLabel(text)
    text_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    
    layout.addWidget(icon_label)
    layout.addWidget(text_label)
    
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    shadow = QGraphicsDropShadowEffect(btn)
    shadow.setBlurRadius(8)
    shadow.setXOffset(0)
    shadow.setYOffset(2)
    shadow.setColor(QColor(0, 0, 0, 30))
    btn.setGraphicsEffect(shadow)
    
    btn.set_labels(icon_label, text_label)
    
    setattr(btn, "icon_label", icon_label)
    setattr(btn, "text_label", text_label)
    
    return btn
