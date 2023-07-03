from dataclasses import dataclass
from enum import Enum


class YMode(Enum):
    DYNMAP = 0,
    JOURNEYMAP = 1


@dataclass(init=True)
class TileStitchArgs:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    tile_width: int
    tile_height: int
    diff: int
    y_mode: YMode
