#!/usr/bin/env python
#coding:utf-8

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class ContainerExecuter():

    # --- カラーパレット ---
    # ベースカラー
    COLOR_WHITE = "#FFFFFF"
    COLOR_BG_LIGHT = "#F5F7FA"  # 背景色をわずかに青みがかった白に
    COLOR_TEXT = "#333333"  # 標準テキスト色を真っ黒ではなく深い灰色に

    # アクセントカラー
    COLOR_PRIMARY = "#2196F3"  # メインカラー（鮮やかな青）
    COLOR_PRIMARY_DARK = "#1565C0"  # 濃い青（ホバー時など）
    COLOR_PRIMARY_LIGHT = "#BBDEFB"  # 薄い青（背景アクセントなど）

    # ステータスカラー
    COLOR_SUCCESS = "#4CAF50"  # 成功/実行中 (緑)
    COLOR_WARNING = "#FF9800"  # 警告 (オレンジ)
    COLOR_ERROR = "#F44336"  # エラー/停止中 (赤)
    COLOR_INFO = "#03A9F4"  # 情報 (水色)

    # UI要素カラー
    COLOR_HOVER = "#E3F2FD"  # ホバー時の背景色
    COLOR_DISABLED = "#ECEFF1"  # 無効時の背景色
    COLOR_DISABLED_TEXT = "#90A4AE"  # 無効時のテキスト色
    COLOR_CONTAINER_ROW_ALT = "#FAFBFC"  # 交互の行の背景色
    COLOR_BORDER = "#E0E0E0"  # ボーダー色

    # --- サイズと間隔の定数 ---
    PADDING_SMALL = 4
    PADDING_MEDIUM = 8
    PADDING_LARGE = 12
    BORDER_RADIUS = 6  # ボタンの角丸半径
    BUTTON_WIDTH = 8
    BUTTON_HEIGHT = 1

    def __init__(self):
        self.tk = tk.Tk()
        self.running_containers_info = []
        self.containers_info = []
        self.iconfile = None

        # アイコン設定
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

        # ウィンドウ設定
        self.tk.title("Container Manager")
        self.tk.configure(bg=self.COLOR_BG_LIGHT)
        self.tk.resizable(True, True)

        # システムのスケーリング情報を取得して適用
        self.scale_factor = self.tk.winfo_fpixels('1i') / 72
        self.font_size = int(9 * self.scale_factor)

        # フォント設定
        self.font_normal = ('Helvetica', self.font_size)
        self.font_bold = ('Helvetica', self.font_size, 'bold')
        self.font_small = ('Helvetica', int(self.font_size * 0.9))
        self.font_title = ('Helvetica', int(self.font_size * 1.2), 'bold')

        # スタイルの設定
        self.setup_styles()

        # メッセージ表示用のラベル（フッター部分）
        self.message_frame = ttk.Frame(self.tk, style='Footer.TFrame')
        self.message_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_indicator = ttk.Label(self.message_frame, text="●",
                                          style='Ready.Status.TLabel', width=2)
        self.status_indicator.pack(side=tk.LEFT, padx=(self.PADDING_MEDIUM, 0))

        self.message_label = ttk.Label(self.message_frame, text="準備完了",
                                       style='Message.TLabel')
        self.message_label.pack(side=tk.LEFT, fill=tk.X,
                                padx=self.PADDING_MEDIUM, pady=self.PADDING_MEDIUM)

        # GUI要素の作成
        self.create_gui_elements()

        # 最初のウィンドウサイズ計算後に適切なサイズに設定
        self.tk.update_idletasks()
        self.calculate_and_set_window_size()

    def calculate_and_set_window_size(self):
        """コンテンツに合わせた最適なウィンドウサイズを計算して設定"""
        # 必要な幅を計算
        min_width = 580  # 最低限必要な幅（調整可能）

        # コンテナリストの幅とボタンの幅に基づいて調整
        if hasattr(self, 'container_list_frame'):
            # コンテナリストが存在する場合はその幅を取得
            frame_width = self.container_list_frame.winfo_reqwidth()
            # 余裕を持たせて幅を設定
            min_width = max(min_width, frame_width + 40)

        # 高さは固定値でも良いが、コンテナ数に応じて調整する
        min_height = 300  # 最低限の高さ
        container_count = len(self.containers_info)

        # コンテナ1つあたりの高さを概算
        container_height = 60  # 各コンテナ行の高さ概算

        # 最大5つのコンテナを表示するのに適した高さ
        target_height = min(min_height + container_count * container_height, min_height + 5 * container_height)

        # ウィンドウサイズを設定
        self.tk.geometry(f"{min_width}x{int(target_height)}")

    def setup_styles(self):
        """スタイルの設定"""
        style = ttk.Style()
        style.theme_use('clam')  # モダンなテーマを選択

        # 基本的なフレームスタイル
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

        # ラベルスタイル
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

        # ステータスインジケーター
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

        # コンテナステータスラベル
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

        # コンテナ名ラベル
        style.configure('Container.Name.TLabel',
                        background=self.COLOR_WHITE,
                        foreground=self.COLOR_TEXT,
                        font=self.font_bold)
        style.configure('ContainerAlt.Name.TLabel',
                        background=self.COLOR_CONTAINER_ROW_ALT,
                        foreground=self.COLOR_TEXT,
                        font=self.font_bold)

        # ボタンスタイル - 基本
        style.configure('TButton',
                        font=self.font_normal,
                        background=self.COLOR_PRIMARY,
                        foreground=self.COLOR_WHITE,
                        borderwidth=0,
                        relief="flat",
                        padding=(self.PADDING_MEDIUM, self.PADDING_SMALL))

        # ボタンのマッピング（状態に応じた変化）
        style.map('TButton',
            foreground=[('pressed', self.COLOR_WHITE),
                        ('active', self.COLOR_WHITE),
                        ('disabled', self.COLOR_DISABLED_TEXT)],
            background=[('pressed', self.COLOR_PRIMARY_DARK),
                        ('active', self.COLOR_PRIMARY_DARK),
                        ('disabled', self.COLOR_DISABLED)],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')])

        # アクションボタンのスタイル
        style.configure('Action.TButton',
                        font=self.font_normal,
                        borderwidth=0)

        # 特定のアクションボタンのスタイル
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

        # ツールバーボタンのスタイル
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
        """GUI要素を作成する"""
        # 既存のGUI要素を全てクリア (message_frame は残す)
        for widget in self.tk.winfo_children():
            if widget != self.message_frame:
                widget.destroy()

        # コンテナ情報を取得
        self.get_containers_info(is_running=False)
        self.get_containers_info(is_running=True)

        # --- ヘッダーフレーム ---
        header_frame = ttk.Frame(self.tk, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, self.PADDING_MEDIUM))

        header_label = ttk.Label(header_frame, text="Docker Container Manager",
                                 style='Header.TLabel')
        header_label.pack(side=tk.LEFT, padx=self.PADDING_MEDIUM)

        # --- ツールバーフレーム ---
        toolbar_frame = ttk.Frame(self.tk, style='TFrame')
        toolbar_frame.pack(fill=tk.X, padx=self.PADDING_MEDIUM,
                           pady=(0, self.PADDING_MEDIUM))

        # 更新ボタン
        refresh_btn = ttk.Button(toolbar_frame, text="更新",
                                command=self.refresh_gui,
                                style='Toolbar.TButton',
                                width=self.BUTTON_WIDTH)
        refresh_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))

        # 閉じるボタン
        close_btn = ttk.Button(toolbar_frame, text="閉じる",
                              command=self.quit_gui,
                              style='Toolbar.TButton',
                              width=self.BUTTON_WIDTH)
        close_btn.pack(side=tk.LEFT)

        # --- コンテナリストのメインフレーム ---
        content_frame = ttk.Frame(self.tk, style='Content.TFrame')
        content_frame.pack(expand=True, fill=tk.BOTH,
                           padx=self.PADDING_MEDIUM,
                           pady=(0, self.PADDING_MEDIUM))

        # --- スクロール付きキャンバス ---
        container_canvas = tk.Canvas(content_frame,
                                    bg=self.COLOR_WHITE,
                                    highlightthickness=0)
        container_scrollbar = ttk.Scrollbar(content_frame,
                                           orient=tk.VERTICAL,
                                           command=container_canvas.yview)
        container_canvas.configure(yscrollcommand=container_scrollbar.set)

        container_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        container_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # --- コンテナリストフレーム ---
        self.container_list_frame = ttk.Frame(container_canvas, style='Container.TFrame')
        container_canvas.create_window((0, 0), window=self.container_list_frame, anchor=tk.NW)

        # リストを固定幅のグリッドレイアウトで構成
        self.container_list_frame.columnconfigure(0, minsize=70)  # 状態列
        self.container_list_frame.columnconfigure(1, weight=1, minsize=200)  # コンテナ名列（伸縮可能）
        self.container_list_frame.columnconfigure(2, minsize=250)  # ボタン列

        # コンテナリストのヘッダー
        header_style = {'pady': self.PADDING_MEDIUM, 'sticky': tk.W}

        ttk.Label(self.container_list_frame, text="状態", style='TLabel').grid(
            row=0, column=0, padx=(self.PADDING_MEDIUM, 0), **header_style)
        ttk.Label(self.container_list_frame, text="コンテナ名", style='TLabel').grid(
            row=0, column=1, padx=self.PADDING_MEDIUM, **header_style)
        ttk.Label(self.container_list_frame, text="アクション", style='TLabel').grid(
            row=0, column=2, padx=self.PADDING_MEDIUM, **header_style)

        # 区切り線
        separator = ttk.Separator(self.container_list_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky='ew',
                      pady=(0, self.PADDING_MEDIUM))

        # フレームのサイズが変更されたらCanvasのスクロール領域を再計算
        self.container_list_frame.bind("<Configure>",
                                      lambda e: container_canvas.configure(
                                          scrollregion=container_canvas.bbox("all")))

        # コンテナ情報表示
        self.display_containers(start_row=2)

        # キャンバスの再描画
        self.tk.update_idletasks()
        container_canvas.configure(scrollregion=container_canvas.bbox("all"))

    def display_containers(self, start_row):
        """コンテナリストを表示する"""
        self.container_widgets = {}

        if not self.containers_info:
            # コンテナが見つからない場合のメッセージ
            ttk.Label(self.container_list_frame,
                     text="コンテナが見つかりません。",
                     style='TLabel').grid(
                row=start_row, column=0, columnspan=3,
                pady=self.PADDING_LARGE, padx=self.PADDING_MEDIUM)
            return

        # 各コンテナごとのウィジェット生成
        for i, container_info in enumerate(self.containers_info):
            row_index = start_row + i
            container_id = container_info[0]

            # コンテナ名の取得
            container_name = container_id[:12]  # IDの短縮形をデフォルト名とする
            if len(container_info) > 6:
                name_part = container_info[6].strip()
                if name_part and name_part != container_id:
                    container_name = name_part

            # 実行中かどうかの確認
            is_running = any(container_id == running_info[0]
                            for running_info in self.running_containers_info)

            # 交互の行の背景色を設定
            row_style = 'Container'
            if i % 2 == 1:
                row_style = 'ContainerAlt'

            widgets = {}

            # 状態表示
            status_text = "実行中" if is_running else "停止中"
            # 交互行を考慮したスタイル選択
            status_style = f'{"Running" if is_running else "Stopped"}{"Alt" if i % 2 == 1 else ""}.Status.TLabel'
            status_label = ttk.Label(self.container_list_frame, text=status_text, style=status_style)
            status_label.grid(row=row_index, column=0, padx=(self.PADDING_MEDIUM, 0),
                             pady=self.PADDING_MEDIUM, sticky=tk.W)
            widgets["status_label"] = status_label

            # コンテナ名ラベル
            name_label = ttk.Label(self.container_list_frame, text=container_name,
                                  style=f'{row_style}.Name.TLabel')
            name_label.grid(row=row_index, column=1, padx=self.PADDING_MEDIUM,
                           pady=self.PADDING_MEDIUM, sticky=tk.W)
            widgets["name_label"] = name_label

            # ボタンフレーム - ボタンを揃えて配置するためのフレーム
            button_frame = ttk.Frame(self.container_list_frame,
                                   style=f'ButtonFrame{"Alt" if i % 2 == 1 else ""}.TFrame')
            button_frame.grid(row=row_index, column=2, padx=self.PADDING_MEDIUM,
                             pady=self.PADDING_MEDIUM, sticky=tk.W)

            # --- 操作ボタン --- ボタン幅を統一
            button_width = 7

            # Startボタン
            start_btn = ttk.Button(button_frame, text="Start", width=button_width,
                                  command=lambda cid=container_id:
                                      self.execute_docker_command("start", cid),
                                  style='Start.Action.TButton',
                                  state=tk.DISABLED if is_running else tk.NORMAL)
            start_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["start_btn"] = start_btn

            # Restartボタン
            restart_btn = ttk.Button(button_frame, text="Restart", width=button_width,
                                    command=lambda cid=container_id:
                                        self.execute_docker_command("restart", cid),
                                    style='Restart.Action.TButton',
                                    state=tk.NORMAL if is_running else tk.DISABLED)
            restart_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["restart_btn"] = restart_btn

            # Stopボタン
            stop_btn = ttk.Button(button_frame, text="Stop", width=button_width,
                                 command=lambda cid=container_id:
                                     self.execute_docker_command("stop", cid),
                                 style='Stop.Action.TButton',
                                 state=tk.NORMAL if is_running else tk.DISABLED)
            stop_btn.pack(side=tk.LEFT, padx=(0, self.PADDING_MEDIUM))
            widgets["stop_btn"] = stop_btn

            # Execボタン
            exec_btn = ttk.Button(button_frame, text="Exec", width=button_width,
                                 command=lambda cid=container_id:
                                     self.execute_docker_command("exec", cid),
                                 style='Exec.Action.TButton',
                                 state=tk.NORMAL if is_running else tk.DISABLED)
            exec_btn.pack(side=tk.LEFT)
            widgets["exec_btn"] = exec_btn

            self.container_widgets[container_id] = widgets

    def execute_docker_command(self, operation, container_id):
        """Dockerコマンドを実行する関数"""
        # コマンド実行中は操作ボタンを無効化する
        if container_id in self.container_widgets:
            widgets = self.container_widgets[container_id]
            # Exec 以外のボタンを無効化 (Execは別ウィンドウを開くため無効化しない方が操作を妨げない)
            buttons_to_disable = ["start_btn", "restart_btn", "stop_btn"]
            if operation != "exec":
                for btn_key in buttons_to_disable:
                    if btn_key in widgets:
                        widgets[btn_key]['state'] = tk.DISABLED
            else:
                # Exec ボタンだけを対象にする場合
                if "exec_btn" in widgets:
                    widgets["exec_btn"]['state'] = tk.DISABLED

        # ステータスインジケーターを更新
        self.status_indicator.config(text="●", style='Warning.Status.TLabel')
        self.update_message(f"コンテナ [{container_id[:12]}] の {operation} コマンドを実行中...",
                           self.COLOR_WARNING)

        # コマンド実行を別スレッドで行い、GUIがブロックされないようにする
        thread = threading.Thread(target=self._run_command_in_thread,
                                args=(operation, container_id))
        thread.daemon = True  # メインスレッド終了時にスレッドも終了
        thread.start()

    def _run_command_in_thread(self, operation, container_id):
        """別スレッドでDockerコマンドを実行し、完了後にGUIを更新する"""
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
            # Exec の場合はGUIスレッドでボタンをすぐに有効化する
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

                    # コマンド完了後にGUIを更新し、ボタンの状態を最新にする
                    self.tk.after(0, self.refresh_gui)

            except Exception as e:
                print(f"コマンドの実行中に例外が発生しました: {e}")
                self.tk.after(0, lambda: self.update_status_error(
                    f"コマンド実行中にエラーが発生しました: {e}"))
                self.tk.after(0, self.refresh_gui)  # エラーでも念のためGUI更新

    def update_message(self, message, color=None):
        """ステータスバーのメッセージを更新する (GUIスレッドから呼び出すこと)"""
        # 色が指定されなかった場合はデフォルトの色
        if color is None:
            color = self.COLOR_TEXT
        self.message_label.config(text=message, foreground=color)

    def update_status_success(self, message):
        """成功メッセージを表示"""
        self.status_indicator.config(text="●", style='Success.Status.TLabel')
        self.update_message(message, self.COLOR_SUCCESS)

    def update_status_error(self, message):
        """エラーメッセージを表示"""
        self.status_indicator.config(text="●", style='Error.Status.TLabel')
        self.update_message(message, self.COLOR_ERROR)

    def update_status_info(self, message):
        """情報メッセージを表示"""
        self.status_indicator.config(text="●", style='Ready.Status.TLabel')
        self.update_message(message, self.COLOR_INFO)

    def quit_gui(self):
        """アプリケーションを終了する"""
        print("[close] button has been clicked.")
        self.tk.quit()
        self.tk.destroy()

    def refresh_gui(self):
        """GUI要素を更新する"""
        print("[refresh] button has been clicked.")
        self.create_gui_elements()
        self.update_status_info("リストを更新しました")

    def get_containers_info(self, is_running=False):
        """Dockerコンテナ情報を取得する"""
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
                self.containers_
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