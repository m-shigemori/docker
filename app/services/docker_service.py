import subprocess
from typing import List, Optional
from app.models.container import Container

class DockerService:
    def _run_docker_command(self, args: List[str], check: bool = True, capture: bool = False) -> Optional[subprocess.CompletedProcess]:
        try:
            return subprocess.run(
                ["docker"] + args,
                capture_output=capture,
                text=True,
                check=check
            )
        except subprocess.CalledProcessError:
            return None

    def list_containers(self) -> List[Container]:
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

    def start_container(self, container_id: str) -> None:
        self._run_docker_command(["start", container_id])

    def stop_container(self, container_id: str) -> None:
        self._run_docker_command(["stop", "--timeout=1", container_id])

    def open_container_shell(self, container_id: str) -> None:
        cmd = f"gnome-terminal -- bash -c 'docker exec -it {container_id} /bin/bash; bash'"
        subprocess.Popen(cmd, shell=True)

    def remove_container(self, container_id: str) -> None:
        self._run_docker_command(["rm", "-f", container_id])

    def remove_image(self, image_name: str) -> None:
        self._run_docker_command(["rmi", image_name])
