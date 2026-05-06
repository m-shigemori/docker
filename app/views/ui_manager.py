import os
import random
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QBrush, QPen, QPainterPath
from PyQt6.QtCore import Qt, QRect, QPoint
from PIL import Image, ImageFilter

class UIManager:
    def __init__(self, master):
        self.master = master
        
        img_dir = "assets/img"
        images = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".jpg")]
        
        self.raw_image = Image.open(random.choice(images))
        self.bg_label = QLabel(self.master)
        self.fg_label = QLabel(self.master)
        self.panel_bg = QLabel(self.master)
        self.control_panel = QFrame(self.master)

    def update(self, w, h):
        if w <= 0 or h <= 0:
            return 0

        bg_img = self._crop_fit(self.raw_image, w, h, blur=True)
        bg_pixmap = self._pil_to_pixmap(bg_img)
        self.bg_label.setPixmap(bg_pixmap)
        self.bg_label.setGeometry(0, 0, w, h)
        self.bg_label.lower()

        fg_img = self._height_fit(self.raw_image, h)
        fg_w = fg_img.width
        fg_pixmap = self._pil_to_pixmap(fg_img)
        self.fg_label.setPixmap(fg_pixmap)
        self.fg_label.setGeometry(w - fg_w, 0, fg_w, h)
        self.fg_label.raise_()

        available_w = w - fg_w
        margin = 10
        
        panel_w = int(available_w - margin * 2)
        panel_h = int(h - margin * 2)
        panel_x = margin
        panel_y = margin

        if panel_w > 0 and panel_h > 0:
            panel_region = bg_img.crop((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h))
            panel_pixmap = self._create_glass_pixmap(panel_region, panel_w, panel_h)
            
            self.panel_bg.setPixmap(panel_pixmap)
            self.panel_bg.setGeometry(panel_x, panel_y, panel_w, panel_h)
            self.panel_bg.raise_()

            self.control_panel.setGeometry(panel_x, panel_y, panel_w, panel_h)
            self.control_panel.setStyleSheet("background: transparent; border: none;")
            self.control_panel.raise_()
        
        return fg_w

    def _pil_to_pixmap(self, pil_img):
        if pil_img.mode != "RGBA":
            pil_img = pil_img.convert("RGBA")
        
        data = pil_img.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(qimage)

    def _create_glass_pixmap(self, region_img, w, h):
        base_pixmap = self._pil_to_pixmap(region_img)
        
        canvas = QPixmap(w, h)
        canvas.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, float(w), float(h), 10, 10)
        
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, base_pixmap)
        
        painter.setBrush(QBrush(QColor(0, 0, 0, 200)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
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
