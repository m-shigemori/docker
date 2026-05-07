import subprocess
import shutil
from dataclasses import dataclass

@dataclass
class Container:
    id: str
    name: str
    status: str
    state: str
    image: str

@dataclass
class ImageInfo:
    id: str
    repository: str
    tag: str
    size: str

class DockerService:
    def _run_docker_command(self, args, check=True, capture=False):
        try:
            if capture:
                return subprocess.run(
                    ["docker"] + args,
                    capture_output=True,
                    text=True,
                    check=check
                )
            else:
                return subprocess.run(
                    ["docker"] + args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=check
                )

        except subprocess.CalledProcessError:
            return None

    def list_containers(self):
        args = ["ps", "-a", "--format", "{{.ID}}::{{.Names}}::{{.Status}}::{{.State}}::{{.Image}}"]
        result = self._run_docker_command(args, capture=True)

        if not result or not result.stdout:
            return []

        containers = []

        for line in result.stdout.strip().split('\n'):
            parts = line.split('::')
            if len(parts) == 5:
                containers.append(Container(*parts))

        return containers

    def list_images(self):
        args = ["images", "--format", "{{.ID}}::{{.Repository}}::{{.Tag}}::{{.Size}}"]
        result = self._run_docker_command(args, capture=True)

        if not result or not result.stdout:
            return []

        images = []

        for line in result.stdout.strip().split('\n'):
            parts = line.split('::')
            if len(parts) == 4:
                images.append(ImageInfo(*parts))

        return images

    def start_container(self, container_id):
        self._run_docker_command(["start", container_id])

    def stop_container(self, container_id):
        self._run_docker_command(["stop", "--timeout=1", container_id])

    def open_container_shell(self, container_id):
        exec_cmd = f"docker exec -it {container_id} bash; exec bash"

        if shutil.which("ptyxis"):
            cmd = ["ptyxis", "--new-window", "--", "bash", "-c", exec_cmd]
        elif shutil.which("gnome-terminal"):
            cmd = ["gnome-terminal", "--", "bash", "-c", exec_cmd]
        elif shutil.which("konsole"):
            cmd = ["konsole", "-e", "bash", "-c", exec_cmd]
        elif shutil.which("xfce4-terminal"):
            cmd = ["xfce4-terminal", "-e", f"bash -c '{exec_cmd}'"]
        else:
            cmd = ["x-terminal-emulator", "-e", f"bash -c '{exec_cmd}'"]

        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def remove_container(self, container_id):
        self._run_docker_command(["rm", "-f", container_id])

    def remove_image(self, image_id):
        self._run_docker_command(["rmi", "-f", image_id])
