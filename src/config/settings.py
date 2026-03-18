import os
import random

class StyleConfig:
    BORDER_RADIUS = 8
    BUTTON_HEIGHT = 42
    CONTROL_BUTTON_WIDTH = 90
    ACTION_BUTTON_WIDTH = 36

    MIN_WINDOW_SIZE = (800, 540)
    SIDE_MARGIN = 15
    FRAME_MAX_HEIGHT_RATIO = 0.9

    COLUMN_STRETCH = {
        "state": 3,
        "name": 5,
        "control": 5
    }

    COLORS = {
        "frame_bg": "rgba(0,0,0,0.85)",
        "frame_border": "rgba(255,255,255,0.3)",
        "control_btn": "rgba(60,60,60,0.8)",
        "start_btn": "rgba(46,204,113,0.8)",
        "delete_btn": "rgba(231,76,60,0.8)",
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

    def __init__(self):
        self.img_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "img"
        ))
        self.IMAGE_PATH = ""
        self.refresh_image_path()

    def refresh_image_path(self):
        if os.path.exists(self.img_dir):
            images = [
                os.path.join(self.img_dir, f)
                for f in os.listdir(self.img_dir)
                if f.lower().endswith((".jpg", ".png", ".jpeg"))
            ]

            if len(images) > 1:
                choices = [img for img in images if img != self.IMAGE_PATH]
                self.IMAGE_PATH = random.choice(choices)
            elif images:
                self.IMAGE_PATH = images[0]
