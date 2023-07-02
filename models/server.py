from dataclasses import dataclass


@dataclass(init=True)
class Server:
    name: str
    dynmap_url: str
    journeymap_url: str
    ignore_ssl_cert: bool
