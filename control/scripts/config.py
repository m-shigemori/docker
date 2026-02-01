import os

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

    IMAGE_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "img", "kotone.jpg"
    ))