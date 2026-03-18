from typing import List
from src.domain.container import Container
from src.domain.container_repository import IContainerRepository

class ContainerService:
    def __init__(self, repository: IContainerRepository):
        self._repository = repository

    def list_containers(self) -> List[Container]:
        return self._repository.list_all()

    def start_container(self, container_id: str) -> None:
        self._repository.start(container_id)

    def stop_container(self, container_id: str) -> None:
        self._repository.stop(container_id)

    def open_container_shell(self, container_id: str) -> None:
        self._repository.exec_shell(container_id)

    def remove_container(self, container_id: str) -> None:
        self._repository.remove(container_id)

    def remove_image(self, image_name: str) -> None:
        self._repository.remove_image(image_name)
