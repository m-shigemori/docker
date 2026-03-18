from abc import ABC, abstractmethod
from typing import List
from .container import Container

class IContainerRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Container]:
        pass

    @abstractmethod
    def start(self, container_id: str) -> None:
        pass

    @abstractmethod
    def stop(self, container_id: str) -> None:
        pass

    @abstractmethod
    def exec_shell(self, container_id: str) -> None:
        pass

    @abstractmethod
    def remove(self, container_id: str) -> None:
        pass

    @abstractmethod
    def remove_image(self, image_name: str) -> None:
        pass
