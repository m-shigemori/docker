import os
import random
from PyQt6.QtWidgets import (
    QLabel, QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget,
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QGraphicsColorizeEffect
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QIcon
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation
from PIL import Image, ImageFilter

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
            self.text_label.setStyleSheet(self.normal_style)

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
            else:
                self.text_label.setStyleSheet(self.normal_style)

class UIManager:
    def __init__(self, master):
        self.master = master

        img_dir = "assets/images"
        self.all_image_paths = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".jpg")]

        self.current_image_path = random.choice(self.all_image_paths)
        self.raw_image = Image.open(self.current_image_path)

        self.bg_root = QWidget(self.master)
        self.bg_root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.bg_effect = QGraphicsOpacityEffect(self.bg_root)
        self.bg_effect.setOpacity(1.0)
        self.bg_root.setGraphicsEffect(self.bg_effect)

        self.bg_label = QLabel(self.bg_root)
        self.fg_label = QLabel(self.bg_root)
        self.panel_bg = QLabel(self.bg_root)

        self.control_panel = QFrame(self.master)

        self.is_delete_mode = False
        self.is_animating = False

        self.last_w = 0
        self.last_h = 0

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self.control_panel)
        self.main_layout.setContentsMargins(0, 15, 0, 15)
        self.main_layout.setSpacing(15)

        self.button_row = QWidget()
        self.button_row.setContentsMargins(15, 0, 15, 0)

        self.row_layout = QHBoxLayout(self.button_row)
        self.row_layout.setContentsMargins(5, 5, 5, 10)
        self.row_layout.setSpacing(10)

        self.btn_refresh = self._create_custom_button("Refresh", "assets/icons/reflesh.svg")
        self.btn_toggle = self._create_custom_button("Operation", "assets/icons/play.svg")
        self.btn_close = self._create_custom_button("Close", "assets/icons/close.svg")

        self.btn_refresh.clicked.connect(self.refresh_background)
        self.btn_toggle.clicked.connect(self.toggle_mode)
        self.btn_close.clicked.connect(self.master.window().close)

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
        self.main_layout.addStretch()

    def _create_custom_button(self, text, icon_path):
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

    def toggle_mode(self):
        self.is_delete_mode = not self.is_delete_mode

        if self.is_delete_mode:
            self.btn_toggle.set_text("Delete")
            self.btn_toggle.icon_label.setProperty("path", "assets/icons/bin.svg")
        else:
            self.btn_toggle.set_text("Operation")
            self.btn_toggle.icon_label.setProperty("path", "assets/icons/play.svg")

        icon_s = self.btn_toggle.icon_label.width()
        icon_pix = QIcon(self.btn_toggle.icon_label.property("path")).pixmap(QSize(icon_s, icon_s))
        self.btn_toggle.icon_label.setPixmap(icon_pix)

        self.update_button_styles()

    def refresh_background(self):
        if self.is_animating: return
        self.is_animating = True

        self.fade_anim = QPropertyAnimation(self.bg_effect, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self._swap_background)
        self.fade_anim.start()

    def _swap_background(self):
        if len(self.all_image_paths) > 1:
            new_path = self.current_image_path
            while new_path == self.current_image_path:
                new_path = random.choice(self.all_image_paths)

            self.current_image_path = new_path
            self.raw_image = Image.open(self.current_image_path)

        self.update(self.last_w, self.last_h)

        self.fade_anim = QPropertyAnimation(self.bg_effect, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.finished.connect(lambda: setattr(self, "is_animating", False))
        self.fade_anim.start()

    def update_button_styles(self):
        w = self.control_panel.width()
        h = self.control_panel.height()

        if w <= 0 or h <= 0: return

        m_left, _, m_right, _ = self.main_layout.getContentsMargins()
        spacing = self.row_layout.spacing()

        full_available_w = w - m_left - m_right
        left_area_w = full_available_w * 0.5

        btn_w = (left_area_w - spacing) / 2
        btn_h = max(30, int(h * 0.08))

        fs_by_w = int(btn_w * 0.12)
        fs_by_h = int(btn_h * 0.45)
        fs = max(8, min(fs_by_w, fs_by_h, 20))
        icon_s = int(fs * 1.5)

        btn_style = f"QPushButton {{ background-color: white; border: 1px solid #dcdcdc; border-radius: 8px; }} QPushButton:hover {{ background-color: #4a3a35; }}"

        normal_label_style = f"color: #4a3a35; font-weight: bold; font-size: {fs}px; background: transparent;"
        hover_label_style = f"color: white; font-weight: bold; font-size: {fs}px; background: transparent;"

        for btn in [self.btn_refresh, self.btn_toggle, self.btn_close]:
            btn.setFixedHeight(btn_h)
            btn.setStyleSheet(btn_style)
            btn.set_labels(btn.icon_label, btn.text_label, normal_label_style, hover_label_style)

            icon_pix = QIcon(btn.icon_label.property("path")).pixmap(QSize(icon_s, icon_s))
            btn.icon_label.setPixmap(icon_pix)
            btn.icon_label.setFixedSize(icon_s, icon_s)

        self.btn_refresh.setFixedWidth(int(btn_w))
        self.btn_toggle.setFixedWidth(int(btn_w))
        self.btn_close.setFixedWidth(int(btn_w))

        while self.row_layout.count():
            item = self.row_layout.takeAt(0)
            if item.widget(): item.widget().setParent(None)

        self.row_layout.addWidget(self.btn_refresh)
        self.row_layout.addWidget(self.btn_toggle)
        self.row_layout.addStretch()
        self.row_layout.addWidget(self.btn_close)

    def update(self, w, h):
        if w <= 0 or h <= 0: return

        self.last_w, self.last_h = w, h
        bg_img = self._crop_fit(self.raw_image, w, h, blur=True)

        self.bg_root.setGeometry(0, 0, w, h)
        self.bg_label.setPixmap(self._pil_to_pixmap(bg_img))
        self.bg_label.setGeometry(0, 0, w, h)
        self.bg_label.lower()

        fg_img = self._height_fit(self.raw_image, h)
        fg_w = fg_img.width

        self.fg_label.setPixmap(self._pil_to_pixmap(fg_img))
        self.fg_label.setGeometry(w - fg_w, 0, fg_w, h)
        self.fg_label.raise_()

        available_w = w - fg_w

        if available_w > 0:
            sidebar_region = bg_img.crop((0, 0, available_w, h))

            self.panel_bg.setPixmap(self._create_glass_pixmap(sidebar_region, available_w, h))
            self.panel_bg.setGeometry(0, 0, available_w, h)
            self.panel_bg.raise_()

            self.control_panel.setGeometry(0, 0, available_w, h)
            self.control_panel.raise_()

            self.update_button_styles()

    def _pil_to_pixmap(self, pil_img):
        if pil_img.mode != "RGBA": pil_img = pil_img.convert("RGBA")

        data = pil_img.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)

        return QPixmap.fromImage(qimage)

    def _create_glass_pixmap(self, region_img, w, h):
        base_pixmap = self._pil_to_pixmap(region_img)
        canvas = QPixmap(w, h)
        canvas.fill(Qt.GlobalColor.transparent)

        painter = QPainter(canvas)
        painter.drawPixmap(0, 0, base_pixmap)
        painter.fillRect(0, 0, w, h, QColor(255, 255, 255, 200))
        painter.end()

        return canvas

    def _crop_fit(self, img, tw, th, blur=False):
        iw, ih = img.size

        if blur:
            small_w, small_h = tw // 8, th // 8
            ratio = max(small_w / iw, small_h / ih)

            nw, nh = int(iw * ratio), int(ih * ratio)
            res = img.resize((nw, nh), Image.Resampling.BOX)

            l, t = (nw - small_w) / 2, (nh - small_h) / 2
            crop = res.crop((l, t, l + small_w, t + small_h))

            blurred = crop.filter(ImageFilter.GaussianBlur(2))
            return blurred.resize((tw, th), Image.Resampling.BILINEAR)

        ratio = max(tw / iw, th / ih)
        nw, nh = int(iw * ratio), int(ih * ratio)
        res = img.resize((nw, nh), Image.Resampling.BILINEAR)

        l, t = (nw - tw) / 2, (nh - th) / 2

        return res.crop((l, t, l + tw, t + th))

    def _height_fit(self, img, th):
        iw, ih = img.size
        nw = int(iw * (th / ih))

        return img.resize((nw, th), Image.Resampling.BILINEAR)
