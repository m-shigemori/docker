from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class ContainerRow(QWidget):
    def __init__(self, container, ui, config, on_action):
        super().__init__()
        self.container = container
        self.ui = ui
        self.config = config
        self.on_action = on_action
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        state_label = self.ui.label("Running" if self.container.is_running else "Stopped", "running" if self.container.is_running else "stopped")
        state_label.setAlignment(Qt.AlignCenter)
        state_label.setFixedHeight(self.config.BUTTON_HEIGHT)
        state_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        name_label = self.ui.label(self.container.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFixedHeight(self.config.BUTTON_HEIGHT)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        action_widget = self._create_actions()
        action_widget.setFixedHeight(self.config.BUTTON_HEIGHT)
        action_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(state_label)
        layout.addWidget(name_label)
        layout.addWidget(action_widget)

        layout.setStretch(0, self.config.COLUMN_STRETCH["state"])
        layout.setStretch(1, self.config.COLUMN_STRETCH["name"])
        layout.setStretch(2, self.config.COLUMN_STRETCH["control"])

    def _create_actions(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)

        if self.container.is_running:
            for text, action in [("■", "stop"), ("⚡", "exec")]:
                btn = self.ui.button(text)
                btn.setFixedHeight(self.config.BUTTON_HEIGHT)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.clicked.connect(lambda _, a=action: self.on_action(a, self.container.id))
                layout.addWidget(btn)
        else:
            btn = self.ui.button("▶ Start", "start")
            btn.setFixedHeight(self.config.BUTTON_HEIGHT)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda: self.on_action("start", self.container.id))
            layout.addWidget(btn)
        return widget