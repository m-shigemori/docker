import os
from PyQt5.QtWidgets import QLabel, QGraphicsBlurEffect, QGraphicsOpacityEffect, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QPixmap

class UIManager:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        self.bg_label = QLabel(parent)
        self.bg_label.setScaledContents(False)

        self.bg_blur = QGraphicsBlurEffect()
        self.bg_blur.setBlurRadius(20)
        self.bg_label.setGraphicsEffect(self.bg_blur)

        self.fade_overlay = QFrame(parent)
        self.fade_overlay.setStyleSheet("background-color: black;")
        self.fade_overlay.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.bg_opacity = QGraphicsOpacityEffect()
        self.bg_opacity.setOpacity(0.0)
        self.fade_overlay.setGraphicsEffect(self.bg_opacity)

        self.side_opacity = QGraphicsOpacityEffect()
        self.side_opacity.setOpacity(1.0)

        self.fade_group = QParallelAnimationGroup()

        self.bg_fade = QPropertyAnimation(self.bg_opacity, b"opacity")
        self.side_fade = QPropertyAnimation(self.side_opacity, b"opacity")

        for anim in [self.bg_fade, self.side_fade]:
            anim.setDuration(500)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            self.fade_group.addAnimation(anim)

    def update_background(self, img_label, left_panel):
        if not os.path.exists(self.config.IMAGE_PATH):
            return

        img_label.setGraphicsEffect(self.side_opacity)

        pixmap = QPixmap(self.config.IMAGE_PATH)
        w = self.parent.width()
        h = self.parent.height()

        scale = max(w / pixmap.width(), h / pixmap.height())
        nw = int(pixmap.width() * scale)
        nh = int(pixmap.height() * scale)
        ox = int((w - nw) / 2)
        oy = int((h - nh) / 2)

        scaled_bg = pixmap.scaled(nw, nh, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.bg_label.setPixmap(scaled_bg)
        self.bg_label.setGeometry(ox, oy, nw, nh)

        self.fade_overlay.setGeometry(0, 0, w, h)
        self.fade_overlay.raise_()
        self.bg_label.lower()

        side = pixmap.scaledToHeight(h, Qt.SmoothTransformation)
        img_label.setPixmap(side)
        img_label.setFixedWidth(side.width())

        if left_panel:
            pw = w - side.width() - (self.config.SIDE_MARGIN * 2)
            left_panel.setFixedWidth(pw)
            left_panel.setFixedHeight(h - 40)
            left_panel.raise_()
            img_label.raise_()

    def fade_refresh(self, on_mid):
        self.fade_group.stop()

        self.bg_fade.setStartValue(0.0)
        self.side_fade.setStartValue(1.0)
        self.bg_fade.setEndValue(1.0)
        self.side_fade.setEndValue(0.0)

        def on_finished():
            self.fade_group.finished.disconnect(on_finished)
            on_mid()
            self.bg_fade.setStartValue(1.0)
            self.side_fade.setStartValue(0.0)
            self.bg_fade.setEndValue(0.0)
            self.side_fade.setEndValue(1.0)
            self.fade_group.start()

        self.fade_group.finished.connect(on_finished)
        self.fade_group.start()
