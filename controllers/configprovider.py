import json
import os

from models.config import Config
from models.server import Server


class ConfigProvider:
    def __init__(self, config: Config, config_dir: str, filename: str):
        self.config = config
        self.config_dir = config_dir
        self.filename = filename

    def ensure_dir_exists(self):
        os.makedirs(self.config_dir, exist_ok=True)

    def read_config(self):
        self.ensure_dir_exists()

        try:
            with open(os.path.join(self.config_dir, self.filename), 'r') as f:
                config = json.load(f)
                self.config.servers = []
                for server in config['servers']:
                    self.config.servers.append(Server(
                        server['name'], server['dynmap_url'], server['journeymap_url'], server['ignore_ssl_cert']
                    ))
        except (OSError, json.JSONDecodeError, KeyError):
            self.config.servers = []

    def save_config(self):
        self.ensure_dir_exists()

        with open(os.path.join(self.config_dir, self.filename), 'w') as f:
            json.dump(self.config, f, default=vars)
