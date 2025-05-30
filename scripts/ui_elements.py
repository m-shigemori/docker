import tkinter as tk
from tkinter import ttk, messagebox
from .constants import (
    COLOR_WHITE, COLOR_BG_LIGHT, COLOR_TEXT, COLOR_PRIMARY, COLOR_PRIMARY_DARK,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_INFO, COLOR_HOVER,
    COLOR_DISABLED, COLOR_DISABLED_TEXT, COLOR_CONTAINER_ROW_ALT,
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE, BUTTON_WIDTH
)

class UIManager:
    def __init__(self, master, docker_service):
        self.master = master
        self.docker_service = docker_service
        self.docker_service.set_ui_callback(self._handle_docker_ui_update)
        self.container_widgets = {}
        self.message_label = None
        self.status_indicator = None
        self.container_list_frame = None

        self.scale_factor = self.master.winfo_fpixels('1i') / 72
        self.font_size = int(9 * self.scale_factor)

        self.font_normal = ('Helvetica', self.font_size)
        self.font_bold = ('Helvetica', self.font_size, 'bold')
        self.font_small = ('Helvetica', int(self.font_size * 0.9))
        self.font_title = ('Helvetica', int(self.font_size * 1.2), 'bold')

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=COLOR_BG_LIGHT)
        style.configure('Footer.TFrame', background=COLOR_WHITE, relief='raised', borderwidth=1)
        style.configure('Header.TFrame', background=COLOR_PRIMARY, relief='flat')
        style.configure('Content.TFrame', background=COLOR_WHITE, relief='flat', borderwidth=1)
        style.configure('Container.TFrame', background=COLOR_WHITE, relief='flat', borderwidth=0)
        style.configure('ContainerAlt.TFrame', background=COLOR_CONTAINER_ROW_ALT, relief='flat', borderwidth=0)
        style.configure('ButtonFrame.TFrame', background=COLOR_WHITE)
        style.configure('ButtonFrameAlt.TFrame', background=COLOR_CONTAINER_ROW_ALT)

        style.configure('TLabel', background=COLOR_BG_LIGHT, foreground=COLOR_TEXT, font=self.font_normal)
        style.configure('Header.TLabel', background=COLOR_PRIMARY, foreground=COLOR_WHITE, font=self.font_title, padding=PADDING_MEDIUM)
        style.configure('Message.TLabel', background=COLOR_WHITE, foreground=COLOR_TEXT, font=self.font_normal)

        style.configure('Ready.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_INFO, font=self.font_bold)
        style.configure('Success.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_SUCCESS, font=self.font_bold)
        style.configure('Error.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_ERROR, font=self.font_bold)
        style.configure('Warning.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_WARNING, font=self.font_bold)

        style.configure('Running.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_SUCCESS, font=self.font_bold)
        style.configure('Stopped.Status.TLabel', background=COLOR_WHITE, foreground=COLOR_ERROR, font=self.font_bold)
        style.configure('RunningAlt.Status.TLabel', background=COLOR_CONTAINER_ROW_ALT, foreground=COLOR_SUCCESS, font=self.font_bold)
        style.configure('StoppedAlt.Status.TLabel', background=COLOR_CONTAINER_ROW_ALT, foreground=COLOR_ERROR, font=self.font_bold)

        style.configure('Container.Name.TLabel', background=COLOR_WHITE, foreground=COLOR_TEXT, font=self.font_bold)
        style.configure('ContainerAlt.Name.TLabel', background=COLOR_CONTAINER_ROW_ALT, foreground=COLOR_TEXT, font=self.font_bold)

        style.configure('TButton', font=self.font_normal, background=COLOR_PRIMARY, foreground=COLOR_WHITE, borderwidth=0, relief="flat", padding=(PADDING_MEDIUM, PADDING_SMALL))
        style.map('TButton',
            foreground=[('pressed', COLOR_WHITE), ('active', COLOR_WHITE), ('disabled', COLOR_DISABLED_TEXT)],
            background=[('pressed', COLOR_PRIMARY_DARK), ('active', COLOR_PRIMARY_DARK), ('disabled', COLOR_DISABLED)],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        style.configure('Action.TButton', font=self.font_normal, borderwidth=0)
        style.configure('Start.Action.TButton', background=COLOR_SUCCESS)
        style.map('Start.Action.TButton', background=[('pressed', '#388E3C'), ('active', '#43A047'), ('disabled', COLOR_DISABLED)])
        style.configure('Stop.Action.TButton', background=COLOR_ERROR)
        style.map('Stop.Action.TButton', background=[('pressed', '#D32F2F'), ('active', '#E53935'), ('disabled', COLOR_DISABLED)])
        style.configure('Restart.Action.TButton', background=COLOR_WARNING)
        style.map('Restart.Action.TButton', background=[('pressed', '#F57C00'), ('active', '#FB8C00'), ('disabled', COLOR_DISABLED)])
        style.configure('Exec.Action.TButton', background=COLOR_PRIMARY)
        style.map('Exec.Action.TButton', background=[('pressed', COLOR_PRIMARY_DARK), ('active', '#1E88E5'), ('disabled', COLOR_DISABLED)])

        style.configure('Toolbar.TButton', font=self.font_normal, background=COLOR_BG_LIGHT, foreground=COLOR_TEXT, borderwidth=1, relief="raised", padding=(PADDING_MEDIUM, PADDING_SMALL))
        style.map('Toolbar.TButton',
            foreground=[('pressed', COLOR_TEXT), ('active', COLOR_TEXT), ('disabled', COLOR_DISABLED_TEXT)],
            background=[('pressed', COLOR_HOVER), ('active', COLOR_HOVER), ('disabled', COLOR_DISABLED)])

    def create_message_frame(self):
        message_frame = ttk.Frame(self.master, style='Footer.TFrame')
        message_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_indicator = ttk.Label(message_frame, text="●", style='Ready.Status.TLabel', width=2)
        self.status_indicator.pack(side=tk.LEFT, padx=(PADDING_MEDIUM, 0))

        self.message_label = ttk.Label(message_frame, text="準備完了", style='Message.TLabel')
        self.message_label.pack(side=tk.LEFT, fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)

    def calculate_and_set_window_size(self, containers_info):
        min_width = 580
        if hasattr(self, 'container_list_frame') and self.container_list_frame:
            self.master.update_idletasks()
            frame_width = self.container_list_frame.winfo_reqwidth()
            min_width = max(min_width, frame_width + 40)

        min_height = 300
        container_count = len(containers_info)
        container_height = 60

        target_height = min(min_height + container_count * container_height, min_height + 5 * container_height)
        self.master.geometry(f"{min_width}x{int(target_height)}")

    def create_gui_elements(self):
        for widget in self.master.winfo_children():
            if hasattr(self, 'message_label') and widget == self.message_label.master:
                continue
            widget.destroy()

        self.docker_service.get_containers_info(is_running=False)
        self.docker_service.get_containers_info(is_running=True)

        header_frame = ttk.Frame(self.master, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))

        header_label = ttk.Label(header_frame, text="Docker Container Manager", style='Header.TLabel')
        header_label.pack(side=tk.LEFT, padx=PADDING_MEDIUM)

        toolbar_frame = ttk.Frame(self.master, style='TFrame')
        toolbar_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))

        refresh_btn = ttk.Button(toolbar_frame, text="更新", command=self.refresh_gui, style='Toolbar.TButton', width=BUTTON_WIDTH)
        refresh_btn.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))

        close_btn = ttk.Button(toolbar_frame, text="閉じる", command=self.master.quit, style='Toolbar.TButton', width=BUTTON_WIDTH)
        close_btn.pack(side=tk.LEFT)

        content_frame = ttk.Frame(self.master, style='Content.TFrame')
        content_frame.pack(expand=True, fill=tk.BOTH, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))

        container_canvas = tk.Canvas(content_frame, bg=COLOR_WHITE, highlightthickness=0)
        container_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=container_canvas.yview)
        container_canvas.configure(yscrollcommand=container_scrollbar.set)

        container_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        container_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.container_list_frame = ttk.Frame(container_canvas, style='Container.TFrame')
        container_canvas.create_window((0, 0), window=self.container_list_frame, anchor=tk.NW)

        self.container_list_frame.columnconfigure(0, minsize=70)
        self.container_list_frame.columnconfigure(1, weight=1, minsize=200)
        self.container_list_frame.columnconfigure(2, minsize=250)

        header_style = {'pady': PADDING_MEDIUM, 'sticky': tk.W}

        ttk.Label(self.container_list_frame, text="状態", style='TLabel').grid(row=0, column=0, padx=(PADDING_MEDIUM, 0), **header_style)
        ttk.Label(self.container_list_frame, text="コンテナ名", style='TLabel').grid(row=0, column=1, padx=PADDING_MEDIUM, **header_style)
        ttk.Label(self.container_list_frame, text="アクション", style='TLabel').grid(row=0, column=2, padx=PADDING_MEDIUM, **header_style)

        separator = ttk.Separator(self.container_list_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, PADDING_MEDIUM))

        self.container_list_frame.bind("<Configure>", lambda e: container_canvas.configure(scrollregion=container_canvas.bbox("all")))

        self.display_containers(start_row=2)

        self.master.update_idletasks()
        container_canvas.configure(scrollregion=container_canvas.bbox("all"))

    def display_containers(self, start_row):
        self.container_widgets = {}

        if not self.docker_service.containers_info:
            ttk.Label(self.container_list_frame, text="コンテナが見つかりません。", style='TLabel').grid(
                row=start_row, column=0, columnspan=3, pady=PADDING_LARGE, padx=PADDING_MEDIUM)
            return

        for i, container_info in enumerate(self.docker_service.containers_info):
            row_index = start_row + i
            container_id = container_info[0]

            container_name = container_id[:12]
            if len(container_info) > 6:
                name_part = container_info[6].strip()
                if name_part and name_part != container_id:
                    container_name = name_part

            is_running = any(container_id == running_info[0] for running_info in self.docker_service.running_containers_info)

            row_style = 'Container'
            if i % 2 == 1:
                row_style = 'ContainerAlt'

            widgets = {}

            status_text = "実行中" if is_running else "停止中"
            status_style = f'{"Running" if is_running else "Stopped"}{"Alt" if i % 2 == 1 else ""}.Status.TLabel'
            status_label = ttk.Label(self.container_list_frame, text=status_text, style=status_style)
            status_label.grid(row=row_index, column=0, padx=(PADDING_MEDIUM, 0), pady=PADDING_MEDIUM, sticky=tk.W)
            widgets["status_label"] = status_label

            name_label = ttk.Label(self.container_list_frame, text=container_name, style=f'{row_style}.Name.TLabel')
            name_label.grid(row=row_index, column=1, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM, sticky=tk.W)
            widgets["name_label"] = name_label

            button_frame = ttk.Frame(self.container_list_frame, style=f'ButtonFrame{"Alt" if i % 2 == 1 else ""}.TFrame')
            button_frame.grid(row=row_index, column=2, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM, sticky=tk.W)

            button_width = 7

            start_btn = ttk.Button(button_frame, text="Start", width=button_width,
                                   command=lambda cid=container_id, w=widgets: self._on_docker_command("start", cid, w),
                                   style='Start.Action.TButton',
                                   state=tk.DISABLED if is_running else tk.NORMAL)
            start_btn.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
            widgets["start_btn"] = start_btn

            restart_btn = ttk.Button(button_frame, text="Restart", width=button_width,
                                     command=lambda cid=container_id, w=widgets: self._on_docker_command("restart", cid, w),
                                     style='Restart.Action.TButton',
                                     state=tk.NORMAL if is_running else tk.DISABLED)
            restart_btn.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
            widgets["restart_btn"] = restart_btn

            stop_btn = ttk.Button(button_frame, text="Stop", width=button_width,
                                  command=lambda cid=container_id, w=widgets: self._on_docker_command("stop", cid, w),
                                  style='Stop.Action.TButton',
                                  state=tk.NORMAL if is_running else tk.DISABLED)
            stop_btn.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))
            widgets["stop_btn"] = stop_btn

            exec_btn = ttk.Button(button_frame, text="Exec", width=button_width,
                                  command=lambda cid=container_id, w=widgets: self._on_docker_command("exec", cid, w),
                                  style='Exec.Action.TButton',
                                  state=tk.NORMAL if is_running else tk.DISABLED)
            exec_btn.pack(side=tk.LEFT)
            widgets["exec_btn"] = exec_btn

            self.container_widgets[container_id] = widgets

    def _on_docker_command(self, operation, container_id, widgets):
        buttons_to_disable = ["start_btn", "restart_btn", "stop_btn"]
        if operation != "exec":
            for btn_key in buttons_to_disable:
                if btn_key in widgets:
                    widgets[btn_key]['state'] = tk.DISABLED
        else:
            if "exec_btn" in widgets:
                widgets["exec_btn"]['state'] = tk.DISABLED

        self.docker_service.execute_docker_command(operation, container_id, widgets)

    def _handle_docker_ui_update(self, update_type, message=None, widgets=None, operation=None):
        if update_type == "success":
            self.master.after(0, lambda: self.update_status(message, COLOR_SUCCESS, 'Success.Status.TLabel'))
        elif update_type == "error":
            self.master.after(0, lambda: self.update_status(message, COLOR_ERROR, 'Error.Status.TLabel'))
        elif update_type == "warning":
            self.master.after(0, lambda: self.update_status(message, COLOR_WARNING, 'Warning.Status.TLabel'))
            if widgets and operation != "exec":
                buttons_to_disable = ["start_btn", "restart_btn", "stop_btn"]
                for btn_key in buttons_to_disable:
                    if btn_key in widgets:
                        self.master.after(0, lambda w=widgets[btn_key]: w.config(state=tk.DISABLED))
        elif update_type == "info":
            self.master.after(0, lambda: self.update_status(message, COLOR_INFO, 'Ready.Status.TLabel'))
        elif update_type == "refresh_gui":
            self.master.after(0, self.refresh_gui)
        elif update_type == "enable_exec_button":
            if widgets and "exec_btn" in widgets:
                self.master.after(0, lambda: widgets["exec_btn"].config(state=tk.NORMAL))

    def update_status(self, message, color, status_style):
        self.status_indicator.config(text="●", style=status_style)
        self.message_label.config(text=message, foreground=color)

    def refresh_gui(self):
        print("[refresh] button has been clicked.")
        self.create_gui_elements()
        self.update_status("リストを更新しました", COLOR_INFO, 'Ready.Status.TLabel')

    def quit_gui(self):
        print("[close] button has been clicked.")
        self.master.quit()
        self.master.destroy()
