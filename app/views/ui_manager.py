import os
import random
import customtkinter as ctk
from PIL import Image, ImageFilter

class UIManager:
    def __init__(self, master):
        self.master = master
        
        img_dir = "assets/img"
        images = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith(".jpg")]
        
        self.raw_image = Image.open(random.choice(images))
        self.bg_label = None
        self.fg_label = None

    def update(self, w, h):
        if w <= 0 or h <= 0:
            return 0

        bg_img = self._crop_fit(self.raw_image, w, h, blur=True)
        self.bg_ctk = ctk.CTkImage(bg_img, bg_img, size=(w, h))

        if not self.bg_label:
            self.bg_label = ctk.CTkLabel(self.master, text="", image=self.bg_ctk)
            self.bg_label.place(x=0, y=0)
        else:
            self.bg_label.configure(image=self.bg_ctk, width=w, height=h)
        
        self.bg_label.lower()

        fg_img = self._height_fit(self.raw_image, h)
        fg_w = fg_img.width
        self.fg_ctk = ctk.CTkImage(fg_img, fg_img, size=(fg_w, h))

        if not self.fg_label:
            self.fg_label = ctk.CTkLabel(self.master, text="", image=self.fg_ctk)
        else:
            self.fg_label.configure(image=self.fg_ctk, width=fg_w, height=h)
        
        self.fg_label.place(x=w - fg_w, y=0)
        
        return fg_w

    def _crop_fit(self, img, tw, th, blur=False):
        if blur:
            small_w, small_h = tw // 8, th // 8

            iw, ih = img.size
            ratio = max(small_w / iw, small_h / ih)

            nw, nh = int(iw * ratio), int(ih * ratio)
            res = img.resize((nw, nh), Image.BOX)

            l, t = (nw - small_w) / 2, (nh - small_h) / 2
            crop = res.crop((l, t, l + small_w, t + small_h))

            blurred = crop.filter(ImageFilter.GaussianBlur(2))
            return blurred.resize((tw, th), Image.BILINEAR)

        iw, ih = img.size
        ratio = max(tw / iw, th / ih)

        nw, nh = int(iw * ratio), int(ih * ratio)
        res = img.resize((nw, nh), Image.BILINEAR)

        l, t = (nw - tw) / 2, (nh - th) / 2
        return res.crop((l, t, l + tw, t + th))

    def _height_fit(self, img, th):
        iw, ih = img.size
        nw = int(iw * (th / ih))

        return img.resize((nw, th), Image.BILINEAR)

