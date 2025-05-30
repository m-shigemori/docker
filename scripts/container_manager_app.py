import tkinter as tk
import os
from .docker_service import DockerService
from .ui_elements import UIManager
from .constants import (
    COLOR_BG_LIGHT,
)

class ContainerManagerApp:
    def __init__(self):
        self.tk = tk.Tk()
        self.docker_service = DockerService()
        self.ui_manager = UIManager(self.tk, self.docker_service)

        self.tk.title("Container Manager")
        self.tk.configure(bg=COLOR_BG_LIGHT)
        self.tk.resizable(True, True)

        self.ui_manager.setup_styles()
        self.ui_manager.create_message_frame()
        self.ui_manager.create_gui_elements()

        self.tk.update_idletasks()
        self.ui_manager.calculate_and_set_window_size(self.docker_service.containers_info)

    def run(self):
        self.tk.mainloop()

    def refresh_gui(self):
        self.ui_manager.refresh_gui()

    def quit_gui(self):
        self.tk.quit()
        self.tk.destroy()
