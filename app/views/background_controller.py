import os
import random
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt6.QtCore import Qt, QPropertyAnimation
from PIL import Image, ImageFilter

class BackgroundController:
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
        
        self.is_animating = False

    def refresh(self, update_callback):
        if self.is_animating: return
        self.is_animating = True
        
        self.fade_anim = QPropertyAnimation(self.bg_effect, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(lambda: self._swap(update_callback))
        self.fade_anim.start()

    def _swap(self, update_callback):
        if len(self.all_image_paths) > 1:
            new_path = self.current_image_path
            while new_path == self.current_image_path:
                new_path = random.choice(self.all_image_paths)
                
            self.current_image_path = new_path
            self.raw_image = Image.open(self.current_image_path)
            
        update_callback()
        
        self.fade_anim = QPropertyAnimation(self.bg_effect, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.finished.connect(lambda: setattr(self, "is_animating", False))
        self.fade_anim.start()

    def update_geometry(self, w, h):
        self.bg_root.setGeometry(0, 0, w, h)
        
        bg_img = self._crop_fit(self.raw_image, w, h, blur=True)
        self.bg_label.setPixmap(self._pil_to_pixmap(bg_img))
        self.bg_label.setGeometry(0, 0, w, h)
        self.bg_label.lower()
        
        fg_img = self._height_fit(self.raw_image, h)
        fg_w = fg_img.width
        self.fg_label.setPixmap(self._pil_to_pixmap(fg_img))
        self.fg_label.setGeometry(w - fg_w, 0, fg_w, h)
        self.fg_label.raise_()
        
        return fg_w, bg_img

    def update_panel_bg(self, bg_img, available_w, h):
        sidebar_region = bg_img.crop((0, 0, available_w, h))
        self.panel_bg.setPixmap(self._create_glass_pixmap(sidebar_region, available_w, h))
        self.panel_bg.setGeometry(0, 0, available_w, h)
        self.panel_bg.raise_()

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
        painter.fillRect(0, 0, w, h, QColor(255, 255, 255, 160))
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
