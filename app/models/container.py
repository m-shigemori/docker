from dataclasses import dataclass

@dataclass
class Container:
    id: str
    name: str
    status: str
    state: str
    image: str
