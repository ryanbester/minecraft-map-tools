from dataclasses import dataclass

from models.server import Server


@dataclass
class Config:
    servers: list[Server]

    def __init__(self):
        pass
