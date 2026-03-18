import subprocess
from typing import List
from src.domain.container import Container
from src.domain.container_repository import IContainerRepository

class DockerRepository(IContainerRepository):
    def list_all(self) -> List[Container]:
        cmd = ["docker", "ps", "-a", "--format", "{{.ID}}::{{.Names}}::{{.Status}}::{{.State}}::{{.Image}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('::')
            if len(parts) == 5:
                containers.append(Container(
                    id=parts[0],
                    name=parts[1],
                    status=parts[2],
                    state=parts[3],
                    image=parts[4]
                ))
        return containers

    def start(self, container_id: str) -> None:
        subprocess.run(f"docker start {container_id}", shell=True, check=True)

    def stop(self, container_id: str) -> None:
        subprocess.run(f"docker stop --timeout=1 {container_id}", shell=True, check=True)

    def exec_shell(self, container_id: str) -> None:
        cmd = f"gnome-terminal -- bash -c 'docker exec -it {container_id} /bin/bash; bash'"
        subprocess.Popen(cmd, shell=True)

    def remove(self, container_id: str) -> None:
        subprocess.run(f"docker rm -f {container_id}", shell=True, check=True)

    def remove_image(self, image_name: str) -> None:
        subprocess.run(f"docker rmi {image_name}", shell=True, check=True)
