from dataclasses import dataclass

@dataclass
class Credential:
    id: int
    site: str
    username: str
    password: bytes