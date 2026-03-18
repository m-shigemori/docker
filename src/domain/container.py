from dataclasses import dataclass

@dataclass(frozen=True)
class Container:
    id: str
    name: str
    status: str
    state: str
    image: str

    @property
    def is_running(self) -> bool:
        return self.state.lower() == "running"
