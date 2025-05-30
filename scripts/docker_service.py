import subprocess
import threading
import tkinter as tk

class DockerService:
    def __init__(self):
        self.running_containers_info = []
        self.containers_info = []
        self.ui_callback = None

    def set_ui_callback(self, callback):
        self.ui_callback = callback

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
            if self.ui_callback:
                self.ui_callback("error", msg)
            self.running_containers_info = []
            self.containers_info = []
        except subprocess.CalledProcessError as e:
            msg = f"Dockerコマンドの実行に失敗しました: {e.returncode} - {e.stderr if hasattr(e, 'stderr') else ''}"
            if self.ui_callback:
                self.ui_callback("error", msg)
            self.running_containers_info = []
            self.containers_info = []
        except Exception as e:
            msg = f"コンテナ情報の取得中に予期せぬエラーが発生しました: {e}"
            if self.ui_callback:
                self.ui_callback("error", msg)
            self.running_containers_info = []
            self.containers_info = []

    def execute_docker_command(self, operation, container_id, widgets_to_update):
        if self.ui_callback:
            self.ui_callback("warning", f"コンテナ [{container_id[:12]}] の {operation} コマンドを実行中...", widgets_to_update, operation)

        thread = threading.Thread(target=self._run_command_in_thread,
                                 args=(operation, container_id, widgets_to_update))
        thread.daemon = True
        thread.start()

    def _run_command_in_thread(self, operation, container_id, widgets_to_update):
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
            if self.ui_callback:
                self.ui_callback("enable_exec_button", widgets_to_update)

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
            try:
                if operation == "exec":
                    subprocess.Popen(cmd, shell=True)
                    if self.ui_callback:
                        self.ui_callback("success", success_message)
                else:
                    process = subprocess.Popen(cmd, shell=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()

                    output = stdout.decode('utf-8', errors='ignore')
                    error_output = stderr.decode('utf-8', errors='ignore')

                    if process.returncode == 0:
                        if self.ui_callback:
                            self.ui_callback("success", success_message)
                    else:
                        if self.ui_callback:
                            self.ui_callback("error", f"{error_message_prefix} {error_output.strip()}")

                    if self.ui_callback:
                        self.ui_callback("refresh_gui")

            except Exception as e:
                if self.ui_callback:
                    self.ui_callback("error", f"コマンド実行中にエラーが発生しました: {e}")
                if self.ui_callback:
                    self.ui_callback("refresh_gui")
