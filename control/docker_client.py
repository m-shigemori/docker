import subprocess
from dataclasses import dataclass
from typing import List

@dataclass
class ContainerInfo:
    id: str
    name: str
    status: str
    state: str

    @property
    def is_running(self) -> bool:
        return self.state.lower() == "running"

class DockerClient:
    def list_containers(self) -> List[ContainerInfo]:
        cmd = ["docker", "ps", "-a", "--format", "{{.ID}}::{{.Names}}::{{.Status}}::{{.State}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('::')
            if len(parts) == 4:
                containers.append(ContainerInfo(
                    id=parts[0],
                    name=parts[1],
                    status=parts[2],
                    state=parts[3]
                ))
        return containers

    def start(self, container_id: str):
        self._run_cmd(f"docker start {container_id}")

    def stop(self, container_id: str):
        self._run_cmd(f"docker stop {container_id}")

    def exec_shell(self, container_id: str):
        cmd = f"gnome-terminal -- bash -c 'docker exec -it {container_id} /bin/bash; bash'"
        subprocess.Popen(cmd, shell=True)

    def _run_cmd(self, cmd: str):
        subprocess.run(cmd, shell=True, check=True)