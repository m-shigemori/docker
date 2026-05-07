from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from app.views.background_controller import BackgroundController
from app.views.control_panel import ControlPanelManager
from app.views.list_manager import ContainerListManager
from app.services.docker_service import DockerService

class UIManager:
    def __init__(self, master):
        self.master = master
        self.docker = DockerService()
        
        self.bg = BackgroundController(self.master)
        self.panel = ControlPanelManager(self.master)
        self.list = ContainerListManager(self.panel.main_layout)
        
        self.is_delete_mode = False
        self.view_mode = "containers"
        self.last_w, self.last_h = 0, 0
        
        self._setup_connections()
        self.refresh_list()

    def _setup_connections(self):
        self.panel.btn_refresh.clicked.connect(self._on_refresh_clicked)
        self.panel.btn_view_mode.clicked.connect(self._toggle_view)
        self.panel.btn_toggle.clicked.connect(self.toggle_mode)
        self.panel.btn_close.clicked.connect(self.master.window().close)

    def _on_refresh_clicked(self):
        self.bg.refresh(lambda: self.update(self.last_w, self.last_h))
        self.refresh_list()

    def _toggle_view(self):
        self.view_mode = "images" if self.view_mode == "containers" else "containers"
        self.panel.update_view_icon(self.view_mode)
        self.refresh_list()

    def toggle_mode(self):
        self.is_delete_mode = not self.is_delete_mode
        self.panel.toggle_mode(self.is_delete_mode)
        self.refresh_list()

    def refresh_list(self):
        self.list.clear_list()
        
        if self.view_mode == "containers":
            items = self.docker.list_containers()
            for c in items:
                row = self.list.create_row(c.id, c.name, c.state, self.is_delete_mode)
                row.action_triggered.connect(self._handle_action)
                row.style_request.connect(self.list.refresh_row_style)
        else:
            items = self.docker.list_images()
            for img in items:
                name = f"{img.repository}:{img.tag}"
                row = self.list.create_row(img.id, name, img.size, self.is_delete_mode, is_image=True)
                row.action_triggered.connect(self._handle_action)
                row.style_request.connect(self.list.refresh_row_style)
                
        self.update(self.last_w, self.last_h)

    def _handle_action(self, action, item_id):
        if action == "start":
            self.docker.start_container(item_id)
            self.bg.refresh(lambda: self.update(self.last_w, self.last_h))
            self.refresh_list()
        elif action == "stop":
            self.docker.stop_container(item_id)
            self.refresh_list()
        elif action == "exec":
            self.docker.open_container_shell(item_id)
        elif action == "delete":
            if self.view_mode == "containers":
                self.docker.remove_container(item_id)
            else:
                self.docker.remove_image(item_id)
            self.refresh_list()

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
