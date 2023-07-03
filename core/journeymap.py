import os
import urllib
from urllib import request

from models.tilestitchargs import TileStitchArgs, YMode


class JourneyMap:
    @staticmethod
    def get_tile_path(map_type: str, zoom: int, region_x: float, region_y: float):
        return '/tiles/tile.png?x={}&z={}&dimension=minecraft:overworld&mapTypeString={}&zoom={}'.format(int(region_x),
                                                                                                         int(region_y),
                                                                                                         map_type, zoom)

    @staticmethod
    def download_tiles(tiles_dir: str, journeymap_url: str, map_type: str, zoom: int, from_x, from_y, to_x, to_y,
                       progress_callback=None) -> TileStitchArgs:
        diff = 1
        total = ((to_x - from_x) / diff + 1) * ((to_y - from_y) / diff + 1)
        i = 0
        for x in range(from_x, to_x + 1, diff):
            for y in range(from_y, to_y + 1, diff):
                i += 1
                if progress_callback is not None:
                    progress_callback('Downloading ({} of {})'.format(i, int(total)), i, total)

                url = journeymap_url + JourneyMap.get_tile_path(map_type, zoom, x, y)
                urllib.request.urlretrieve(url, os.path.join(tiles_dir, '{}_{}.jpg'.format(x, y)))

        return TileStitchArgs(from_x, from_y, to_x, to_y, 512, 512, diff, YMode.JOURNEYMAP)
