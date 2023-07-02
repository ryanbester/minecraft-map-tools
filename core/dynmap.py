import json
import math
import os
import ssl
import urllib
from typing import Optional
from urllib import request

import validators

from models.server import Server
from models.tilestitchargs import TileStitchArgs


class Dynmap:
    @staticmethod
    def get_config(server: Server) -> dict:
        if server.dynmap_url is None or validators.url(server.dynmap_url) is not True:
            raise ValueError('Incorrect server or no Dynmap URL specified')

        if server.ignore_ssl_cert:
            ssl._create_default_https_context = ssl._create_unverified_context

        with urllib.request.urlopen('{}/up/configuration'.format(server.dynmap_url)) as response:
            return json.load(response)

    @staticmethod
    def get_map_ids(dynmap_config: dict) -> list[str]:
        map_ids = []
        for world in dynmap_config['worlds']:
            for map_obj in world['maps']:
                map_ids.append('{} - {}'.format(world['name'], map_obj['name']))

        return map_ids

    @staticmethod
    def get_map_obj(dynmap_config: dict, map_id: str) -> Optional[dict]:
        map_names = map_id.split(' - ')
        for config_world in dynmap_config['worlds']:
            if config_world['name'] == map_names[0]:
                for config_map in config_world['maps']:
                    if config_map['name'] == map_names[1]:
                        return config_map

        return None

    @staticmethod
    def get_tile_path(world_name: str, map_name: str, zoom: int, tile_x: float, tile_y: float):
        zoom_str = 'z' * zoom
        if len(zoom_str) > 0:
            zoom_str += '_'

        chunk_x = math.floor(tile_x / 32)
        chunk_y = math.floor(tile_y / 32)

        return '/tiles/{}/{}/{}_{}/{}{}_{}.jpg'.format(world_name, map_name, int(chunk_x), int(chunk_y), zoom_str,
                                                       int(tile_x), int(tile_y))

    @staticmethod
    def download_tiles(tiles_dir: str, dynmap_url: str, world_name: str, map_name: str, zoom: int, from_x, from_y,
                       to_x, to_y, progress_callback=None) -> TileStitchArgs:
        diff = 2 ** zoom
        total = ((to_x - from_x) / diff + 1) * ((to_y - from_y) / diff + 1)
        i = 0
        for x in range(from_x, to_x + 1, diff):
            for y in range(from_y, to_y + 1, diff):
                i += 1
                if progress_callback is not None:
                    progress_callback('Downloading ({} of {})'.format(i, int(total)), i, total)

                url = dynmap_url + Dynmap.get_tile_path(world_name, map_name, zoom, x, y)
                urllib.request.urlretrieve(url, os.path.join(tiles_dir, '{}_{}.jpg'.format(x, y)))

        return TileStitchArgs(from_x, from_y, to_x, to_y, 128, 128, diff)
