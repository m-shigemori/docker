import customtkinter as ctk
from app.views.ui_manager import UIManager

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600")
        self.title("ContainerExecuter")

        self.ui = UIManager(self)
        self.update_pending = False

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, e):
        if e.widget == self and not self.update_pending:
            self.update_pending = True
            self.after(10, self.do_update)

    def do_update(self):
        self.render()
        self.update_pending = False

    def render(self):
        self.ui.update(self.winfo_width(), self.winfo_height())
