from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from app.views.background_controller import BackgroundController
from app.views.control_panel import ControlPanelManager
from app.views.list_manager import ContainerListManager

class UIManager:
    def __init__(self, master):
        self.master = master
        
        self.bg = BackgroundController(self.master)
        self.panel = ControlPanelManager(self.master)
        self.list = ContainerListManager(self.panel.main_layout)
        
        self.is_delete_mode = False
        self.last_w, self.last_h = 0, 0
        
        self.dummy_data = [
            {"name": "web-server", "state": "running"},
            {"name": "db-master", "state": "exited"},
            {"name": "cache-node", "state": "running"}
        ]
        
        self._setup_connections()
        self.refresh_list()

    def _setup_connections(self):
        self.panel.btn_refresh.clicked.connect(lambda: self.bg.refresh(lambda: self.update(self.last_w, self.last_h)))
        self.panel.btn_toggle.clicked.connect(self.toggle_mode)
        self.panel.btn_close.clicked.connect(self.master.window().close)

    def toggle_mode(self):
        self.is_delete_mode = not self.is_delete_mode
        self.panel.toggle_mode(self.is_delete_mode)
        self.refresh_list()

    def refresh_list(self):
        self.list.clear_list()
        for data in self.dummy_data:
            self.list.create_container_row(data["name"], data["state"], self.is_delete_mode)
        self.update(self.last_w, self.last_h)

    def update(self, w, h):
        if w <= 0 or h <= 0: return
        self.last_w, self.last_h = w, h
        
        fg_w, bg_img = self.bg.update_geometry(w, h)
        available_w = w - fg_w
        
        if available_w > 0:
            self.bg.update_panel_bg(bg_img, available_w, h)
            self.panel.frame.setGeometry(0, 0, available_w, h)
            self.panel.frame.raise_()
            self._apply_styles(available_w, h)

    def _apply_styles(self, w, h):
        m_left, _, m_right, _ = self.panel.main_layout.getContentsMargins()
        spacing = self.panel.row_layout.spacing()
        
        full_available_w = w - m_left - m_right
        left_area_w = full_available_w * 0.5
        
        btn_h = max(30, int(h * 0.08))
        top_btn_w = (left_area_w - spacing) / 2
        
        action_area_w = full_available_w * (4/9)
        list_btn_w = (action_area_w - 40) / 2
        
        fs = max(8, min(int(list_btn_w * 0.25), int(btn_h * 0.45), 20))
        icon_s = int(fs * 1.5)
        
        styles = {
            "btn": "QPushButton { background-color: white; border: 1px solid #dcdcdc; border-radius: 8px; } QPushButton:hover { background-color: #4a3a35; }",
            "list_btn": "QPushButton { background-color: #fffbe3; border: 1px solid #dcdcdc; border-radius: 8px; } QPushButton:hover { background-color: #4a3a35; }",
            "normal": f"color: #4a3a35; font-weight: bold; font-size: {fs}px; background: transparent;",
            "hover": f"color: white; font-weight: bold; font-size: {fs}px; background: transparent;",
            "header": f"color: #4a3a35; font-weight: bold; font-size: {fs}px; background: transparent;"
        }
        
        self.panel.update_styles(top_btn_w, btn_h, icon_s, styles["btn"], styles["normal"], styles["hover"])
        self.list.update_styles(fs, icon_s, btn_h, styles["list_btn"], styles["hover"], styles["header"], list_btn_w)
