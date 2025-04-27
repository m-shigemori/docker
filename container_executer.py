#!/usr/bin/env python
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class ContainerExecuter():
    COLOR_WHITE = "#FFFFFF"
    COLOR_BG_LIGHT = "#F5F7FA"
    COLOR_TEXT = "#333333"

    COLOR_PRIMARY = "#2196F3"
    COLOR_PRIMARY_DARK = "#1565C0"
    COLOR_PRIMARY_LIGHT = "#BBDEFB"

    COLOR_SUCCESS = "#4CAF50"
    COLOR_WARNING = "#FF9800"
    COLOR_ERROR = "#F44336"
    COLOR_INFO = "#03A9F4"

    COLOR_HOVER = "#E3F2FD"
    COLOR_DISABLED = "#ECEFF1"
    COLOR_DISABLED_TEXT = "#90A4AE"
    COLOR_CONTAINER_ROW_ALT = "#FAFBFC"
    COLOR_BORDER = "#E0E0E0"

    PADDING_SMALL = 4
    PADDING_MEDIUM = 8
    PADDING_LARGE = 12
    BORDER_RADIUS = 6
    BUTTON_WIDTH = 8
    BUTTON_HEIGHT = 1

    def __init__(self):
        self.tk = tk.Tk()
        self.running_containers_info = []
        self.containers_info = []
        self.iconfile = None

        icon_path = os.path.join(os.path.dirname(__file__), 'img', 'docker.png')
        if os.path.exists(icon_path):
            try:
                self.iconfile = tk.PhotoImage(file=icon_path)
                self.tk.call('wm', 'iconphoto', self.tk._w, self.iconfile)
            except tk.TclError:
                print(f"アイコンファイルの読み込みにTclErrorが発生しました: {icon_path}")
                print("tkinterのPhotoImageがこのPNG形式に対応していない可能性があります。")
        else:
            print(f"アイコンファイルが見つかりません: {icon_path}")

        self.tk.title("Container Manager")
        self.tk.configure(bg=self.COLOR_BG_LIGHT)
        self.tk.resizable(True, True)

        self.scale_factor = self.tk.winfo_fpixels('1i') / 72
        self.font_size = int(9 * self.scale_factor)

        self.font_normal = ('Helvetica', self.font_size)
        self.font_bold = ('Helvetica', self.font_size, 'bold')
        self.font_small = ('Helvetica', int(self.font_size * 0.9))
        self.font_title = ('Helvetica', int(self.font_size * 1.2), 'bold')

        self.setup_styles()

        self.message_frame = ttk.Frame(self.tk, style='Footer.TFrame')
        self.message_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_indicator = ttk.Label(self.message_frame, text="●",
                                            style='Ready.Status.TLabel', width=2)
        self.status_indicator.pack(side=tk.LEFT, padx=(self.PADDING_MEDIUM, 0))

        self.message_label = ttk.Label(self.message_frame, text="準備完了",
                                       style='Message.TLabel')
        self.message_label.pack(side=tk.LEFT, fill=tk.X,
                                padx=self.PADDING_MEDIUM, pady=self.PADDING_MEDIUM)

        self.create_gui_elements()

        self.tk.update_idletasks()
        self.calculate_and_set_window_size()

    def calculate_and_set_window_size(self):
        min_width = 580

        if hasattr(self, 'container_list_frame'):
            frame_width = self.container_list_frame.winfo_reqwidth()
            min_width = max(min_width, frame_width + 40)

        min_height = 300
        container_count = len(self.containers_info)

        container_height = 60

        target_height = min(min_height + container_count * container_height, min_height + 5 * container_height)

        self.tk.geometry(f"{min_width}x{int(target_height)}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.COLOR_BG_LIGHT)
        style.configure('Footer.TFrame', background=self.COLOR_WHITE,
                        relief='raised', borderwidth=1)
        style.configure('Header.TFrame', background=self.COLOR_PRIMARY,
                        relief='flat')
        style.configure('Content.TFrame', background=self.COLOR_WHITE,
                        relief='flat', borderwidth=1)
        style.configure('Container.TFrame', background=self.COLOR_WHITE,
                        relief='flat', borderwidth=0)
        style.configure('ContainerAlt.TFrame', background=self.COLOR_CONTAINER_ROW_ALT,
                        relief='flat', borderwidth=0)
        style.configure('ButtonFrame.TFrame', background=self.COLOR_WHITE)
        style.configure('ButtonFrameAlt.TFrame', background=self.COLOR_CONTAINER_ROW_ALT)

        style.configure('TLabel',
                        background=self.COLOR_BG_LIGHT,
                        foreground=self.COLOR_TEXT,
                        font=self.font_normal)
        style.configure('Header.TLabel',
                        background=self.COLOR_PRIMARY,
                        foreground=self.COLOR_WHITE,
                        font=self.font_title,
                        padding=self.PADDING_MEDIUM)
        style.configure('Message.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_TEXT,
                        font=self.font_normal)

        style.configure('Ready.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_INFO,
                        font=self.font_bold)
        style.configure('Success.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_SUCCESS,
                        font=self.font_bold)
        style.configure('Error.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_ERROR,
                        font=self.font_bold)
        style.configure('Warning.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_WARNING,
                        font=self.font_bold)

        style.configure('Running.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_SUCCESS,
                        font=self.font_bold)
        style.configure('Stopped.Status.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_ERROR,
                        font=self.font_bold)
        style.configure('RunningAlt.Status.TLabel',
                        background=self.COLOR_CONTAINER_ROW_ALT,
                        foreground=self.COLOR_SUCCESS,
                        font=self.font_bold)
        style.configure('StoppedAlt.Status.TLabel',
                        background=self.COLOR_CONTAINER_ROW_ALT,
                        foreground=self.COLOR_ERROR,
                        font=self.font_bold)

        style.configure('Container.Name.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_TEXT,
                        font=self.font_bold)
        style.configure('ContainerAlt.Name.TLabel',
                        background=self.COLOR_CONTAINER_ROW_ALT,
                        foreground=self.COLOR_TEXT,
                        font=self.font_bold)

        style.configure('TButton',
                        font=self.font_normal,
                        background=self.COLOR_PRIMARY,
                        foreground=self.COLOR_WHITE,
                        borderwidth=0,
                        relief="flat",
                        padding=(self.PADDING_MEDIUM, self.PADDING_SMALL))

        style.map('TButton',
            foreground=[('pressed', self.COLOR_WHITE),
                        ('active', self.COLOR_WHITE),
                        ('disabled', self.COLOR_DISABLED_TEXT)],
            background=[('pressed', self.COLOR_PRIMARY_DARK),
                        ('active', self.COLOR_PRIMARY_DARK),
                        ('disabled', self.COLOR_DISABLED)],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        style.configure('Action.TButton',
                        font=self.font_normal,
                        borderwidth=0)

        style.configure('Start.Action.TButton', background=self.COLOR_SUCCESS)
        style.map('Start.Action.TButton',
            background=[('pressed', '#388E3C'),
                        ('active', '#43A047'),
                        ('disabled', self.COLOR_DISABLED)])

        style.configure('Stop.Action.TButton', background=self.COLOR_ERROR)
        style.map('Stop.Action.TButton',
            background=[('pressed', '#D32F2F'),
                        ('active', '#E53935'),
                        ('disabled', self.COLOR_DISABLED)])

        style.configure('Restart.Action.TButton', background=self.COLOR_WARNING)
        style.map('Restart.Action.TButton',
            background=[('pressed', '#F57C00'),
                        ('active', '#FB8C00'),
                        ('disabled', self.COLOR_DISABLED)])

        style.configure('Exec.Action.TButton', background=self.COLOR_PRIMARY)
        style.map('Exec.Action.TButton',
            background=[('pressed', self.COLOR_PRIMARY_DARK),
                        ('active', '#1E88E5'),
                        ('disabled', self.COLOR_DISABLED)])

        style.configure('Toolbar.TButton',
                        font=self.font_normal,
                        background=self.COLOR_BG_LIGHT,
                        foreground=self.COLOR_TEXT,
                        borderwidth=1,
                        relief="raised",
                        padding=(self.PADDING_MEDIUM, self.PADDING_SMALL))

        style.map('Toolbar.TButton',
            foreground=[('pressed', self.COLOR_TEXT),
                        ('active', self.COLOR_TEXT),
                        ('disabled', self.COLOR_DISABLED_TEXT)],
            background=[('pressed', self.COLOR_HOVER),
                        ('active', self.COLOR_HOVER),
                        ('disabled', self.COLOR_DISABLED)])

    def create_gui_elements(self):
        for widget in self.tk.winfo_children():
            if widget != self.message_frame:
                widget.destroy()

        self.get_containers_info(is_running=False)
        self.get_containers_info(is_running=True)

        header_frame = ttk.Frame(self.tk, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, self.PADDING_MEDIUM))

        header_label = ttk.Label(header_frame, text="Docker Container Manager",
                                 style='Header.TLabel')
        header_label.pack(side=tk.LEFT, padx=self.PADDING_MEDIUM)

        toolbar_frame = ttk.Frame(self.tk, style='TFrame')
        toolbar_frame.pack(fill=tk.X, padx=self.PADDING_MEDIUM,
                           pady=(0, self.PADDING_MEDIUM))

        refresh_btn = ttk.Button(toolbar_frame, text="更新",
                                 command=self.refresh_gui,
                                 style='Toolbar.TButton',
                                 width=self.BUTTON_WIDTH)
        refresh_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))

        close_btn = ttk.Button(toolbar_frame, text="閉じる",
                               command=self.quit_gui,
                               style='Toolbar.TButton',
                               width=self.BUTTON_WIDTH)
        close_btn.pack(side=tk.LEFT)

        content_frame = ttk.Frame(self.tk, style='Content.TFrame')
        content_frame.pack(expand=True, fill=tk.BOTH,
                           padx=self.PADDING_MEDIUM,
                           pady=(0, self.PADDING_MEDIUM))

        container_canvas = tk.Canvas(content_frame,
                                     bg=self.COLOR_WHITE,
                                     highlightthickness=0)
        container_scrollbar = ttk.Scrollbar(content_frame,
                                            orient=tk.VERTICAL,
                                            command=container_canvas.yview)
        container_canvas.configure(yscrollcommand=container_scrollbar.set)

        container_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        container_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.container_list_frame = ttk.Frame(container_canvas, style='Container.TFrame')
        container_canvas.create_window((0, 0), window=self.container_list_frame, anchor=tk.NW)

        self.container_list_frame.columnconfigure(0, minsize=70)
        self.container_list_frame.columnconfigure(1, weight=1, minsize=200)
        self.container_list_frame.columnconfigure(2, minsize=250)

        header_style = {'pady': self.PADDING_MEDIUM, 'sticky': tk.W}

        ttk.Label(self.container_list_frame, text="状態", style='TLabel').grid(
            row=0, column=0, padx=(self.PADDING_MEDIUM, 0), **header_style)
        ttk.Label(self.container_list_frame, text="コンテナ名", style='TLabel').grid(
            row=0, column=1, padx=self.PADDING_MEDIUM, **header_style)
        ttk.Label(self.container_list_frame, text="アクション", style='TLabel').grid(
            row=0, column=2, padx=self.PADDING_MEDIUM, **header_style)

        separator = ttk.Separator(self.container_list_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky='ew',
                       pady=(0, self.PADDING_MEDIUM))

        self.container_list_frame.bind("<Configure>",
                                     lambda e: container_canvas.configure(
                                         scrollregion=container_canvas.bbox("all")))

        self.display_containers(start_row=2)

        self.tk.update_idletasks()
        container_canvas.configure(scrollregion=container_canvas.bbox("all"))

    def display_containers(self, start_row):
        self.container_widgets = {}

        if not self.containers_info:
            ttk.Label(self.container_list_frame,
                      text="コンテナが見つかりません。",
                      style='TLabel').grid(
                row=start_row, column=0, columnspan=3,
                pady=self.PADDING_LARGE, padx=self.PADDING_MEDIUM)
            return

        for i, container_info in enumerate(self.containers_info):
            row_index = start_row + i
            container_id = container_info[0]

            container_name = container_id[:12]
            if len(container_info) > 6:
                name_part = container_info[6].strip()
                if name_part and name_part != container_id:
                    container_name = name_part

            is_running = any(container_id == running_info[0]
                             for running_info in self.running_containers_info)

            row_style = 'Container'
            if i % 2 == 1:
                row_style = 'ContainerAlt'

            widgets = {}

            status_text = "実行中" if is_running else "停止中"
            status_style = f'{"Running" if is_running else "Stopped"}{"Alt" if i % 2 == 1 else ""}.Status.TLabel'
            status_label = ttk.Label(self.container_list_frame, text=status_text, style=status_style)
            status_label.grid(row=row_index, column=0, padx=(self.PADDING_MEDIUM, 0),
                             pady=self.PADDING_MEDIUM, sticky=tk.W)
            widgets["status_label"] = status_label

            name_label = ttk.Label(self.container_list_frame, text=container_name,
                                   style=f'{row_style}.Name.TLabel')
            name_label.grid(row=row_index, column=1, padx=self.PADDING_MEDIUM,
                            pady=self.PADDING_MEDIUM, sticky=tk.W)
            widgets["name_label"] = name_label

            button_frame = ttk.Frame(self.container_list_frame,
                                     style=f'ButtonFrame{"Alt" if i % 2 == 1 else ""}.TFrame')
            button_frame.grid(row=row_index, column=2, padx=self.PADDING_MEDIUM,
                             pady=self.PADDING_MEDIUM, sticky=tk.W)

            button_width = 7

            start_btn = ttk.Button(button_frame, text="Start", width=button_width,
                                   command=lambda cid=container_id:
                                       self.execute_docker_command("start", cid),
                                   style='Start.Action.TButton',
                                   state=tk.DISABLED if is_running else tk.NORMAL)
            start_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["start_btn"] = start_btn

            restart_btn = ttk.Button(button_frame, text="Restart", width=button_width,
                                     command=lambda cid=container_id:
                                         self.execute_docker_command("restart", cid),
                                     style='Restart.Action.TButton',
                                     state=tk.NORMAL if is_running else tk.DISABLED)
            restart_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["restart_btn"] = restart_btn

            stop_btn = ttk.Button(button_frame, text="Stop", width=button_width,
                                  command=lambda cid=container_id:
                                      self.execute_docker_command("stop", cid),
                                  style='Stop.Action.TButton',
                                  state=tk.NORMAL if is_running else tk.DISABLED)
            stop_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["stop_btn"] = stop_btn

            exec_btn = ttk.Button(button_frame, text="Exec", width=button_width,
                                  command=lambda cid=container_id:
                                      self.execute_docker_command("exec", cid),
                                  style='Exec.Action.TButton',
                                  state=tk.NORMAL if is_running else tk.DISABLED)
            exec_btn.pack(side=tk.LEFT)
            widgets["exec_btn"] = exec_btn

            self.container_widgets[container_id] = widgets

    def execute_docker_command(self, operation, container_id):
        if container_id in self.container_widgets:
            widgets = self.container_widgets[container_id]
            buttons_to_disable = ["start_btn", "restart_btn", "stop_btn"]
            if operation != "exec":
                for btn_key in buttons_to_disable:
                    if btn_key in widgets:
                        widgets[btn_key]['state'] = tk.DISABLED
            else:
                if "exec_btn" in widgets:
                    widgets["exec_btn"]['state'] = tk.DISABLED


        self.status_indicator.config(text="●", style='Warning.Status.TLabel')
        self.update_message(f"コンテナ [{container_id[:12]}] の {operation} コマンドを実行中...",
                           self.COLOR_WARNING)

        thread = threading.Thread(target=self._run_command_in_thread,
                                 args=(operation, container_id))
        thread.daemon = True
        thread.start()

    def _run_command_in_thread(self, operation, container_id):
        container_name = f"ID: {container_id[:12]}"
        for info in self.containers_info:
            if info[0] == container_id and len(info) > 6:
                name_part = info[6].strip()
                if name_part:
                    container_name = name_part
                    break

        cmd = None
        success_message = ""
        error_message_prefix = ""

        if operation == "exec":
            cmd = f"gnome-terminal -- bash -c 'docker exec -it {container_id} /bin/bash; echo -e \"\\nセッションを終了しました\"; read -p \"ターミナルを閉じるにはEnterキーを押してください...\"'"
            success_message = f"コンテナ [{container_name}] でシェルを起動しました。"
            error_message_prefix = f"コンテナ [{container_name}] でシェル起動に失敗しました:"
            if container_id in self.container_widgets:
                widgets = self.container_widgets[container_id]
                if "exec_btn" in widgets:
                    self.tk.after(0, lambda: widgets["exec_btn"].config(state=tk.NORMAL))

        elif operation == "start":
            cmd = f"docker start {container_id}"
            success_message = f"コンテナ [{container_name}] を起動しました。"
            error_message_prefix = f"コンテナ [{container_name}] の起動に失敗しました:"
        elif operation == "restart":
            cmd = f"docker restart {container_id}"
            success_message = f"コンテナ [{container_name}] を再起動しました。"
            error_message_prefix = f"コンテナ [{container_name}] の再起動に失敗しました:"
        elif operation == "stop":
            cmd = f"docker stop {container_id}"
            success_message = f"コンテナ [{container_name}] を停止しました。"
            error_message_prefix = f"コンテナ [{container_name}] の停止に失敗しました:"

        if cmd:
            print(f"Executing: {container_name}")
            try:
                if operation == "exec":
                    subprocess.Popen(cmd, shell=True)
                    self.tk.after(0, lambda: self.update_status_success(success_message))
                else:
                    process = subprocess.Popen(cmd, shell=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()

                    output = stdout.decode('utf-8', errors='ignore')
                    error_output = stderr.decode('utf-8', errors='ignore')

                    if process.returncode == 0:
                        self.tk.after(0, lambda: self.update_status_success(success_message))
                    else:
                        print("Error Output:", error_output)
                        self.tk.after(0, lambda: self.update_status_error(
                            f"{error_message_prefix} {error_output.strip()}"))

                    self.tk.after(0, self.refresh_gui)

            except Exception as e:
                print(f"コマンドの実行中に例外が発生しました: {e}")
                self.tk.after(0, lambda: self.update_status_error(
                    f"コマンド実行中にエラーが発生しました: {e}"))
                self.tk.after(0, self.refresh_gui)


    def update_message(self, message, color=None):
        if color is None:
            color = self.COLOR_TEXT
        self.message_label.config(text=message, foreground=color)

    def update_status_success(self, message):
        self.status_indicator.config(text="●", style='Success.Status.TLabel')
        self.update_message(message, self.COLOR_SUCCESS)

    def update_status_error(self, message):
        self.status_indicator.config(text="●", style='Error.Status.TLabel')
        self.update_message(message, self.COLOR_ERROR)

    def update_status_info(self, message):
        self.status_indicator.config(text="●", style='Ready.Status.TLabel')
        self.update_message(message, self.COLOR_INFO)

    def quit_gui(self):
        print("[close] button has been clicked.")
        self.tk.quit()
        self.tk.destroy()

    def refresh_gui(self):
        print("[refresh] button has been clicked.")
        self.create_gui_elements()
        self.update_status_info("リストを更新しました")

    def get_containers_info(self, is_running=False):
        cmd = "docker ps --no-trunc --format '{{.ID}}\\t{{.Image}}\\t{{.Command}}\\t{{.CreatedAt}}\\t{{.Status}}\\t{{.Ports}}\\t{{.Names}}'"
        if not is_running:
            cmd += " -a"
        try:
            res = subprocess.check_output(cmd, shell=True, text=True)
            output = res.strip()
            lines = output.split("\n")

            info_list = []
            if lines and lines[0]:
                for line in lines:
                    parts = line.split('\t')
                    if parts and len(parts) >= 7:
                        info_list.append(parts)

            if is_running:
                self.running_containers_info = info_list
            else:
                self.containers_info = info_list

        except FileNotFoundError:
            msg = "エラー: 'docker' コマンドが見つかりません。Dockerがインストールされ、PATHが通っているか確認してください。"
            print(msg)
            self.update_status_error(msg)
            if is_running:
                self.running_containers_info = []
            else:
                self.containers_info = []
        except subprocess.CalledProcessError as e:
            msg = f"Dockerコマンドの実行に失敗しました: {e.returncode} - {e.stderr if hasattr(e, 'stderr') else ''}"
            print(msg)
            self.update_status_error(msg)
            if is_running:
                self.running_containers_info = []
            else:
                self.containers_info = []
        except Exception as e:
            msg = f"コンテナ情報の取得中に予期せぬエラーが発生しました: {e}"
            print(msg)
            self.update_status_error(msg)
            if is_running:
                self.running_containers_info = []
            else:
                self.containers_info = []


def main():
    ce = ContainerExecuter()
    ce.tk.mainloop()

if __name__ == "__main__":
    main()