from dataclasses import dataclass


@dataclass(init=True)
class TileStitchArgs:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    tile_width: int
    tile_height: int
    diff: int
