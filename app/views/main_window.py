from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import QSize
from app.views.ui_manager import UIManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(960, 540))
        self.resize(960, 540)
        self.setWindowTitle("")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.ui = UIManager(self.central_widget)

    def resizeEvent(self, event):
        self.ui.update(self.central_widget.width(), self.central_widget.height())
        super().resizeEvent(event)

