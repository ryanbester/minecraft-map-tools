import math


class DynmapCoords:
    scale_div = 128.0

    @staticmethod
    def mc_to_tile(map_obj: dict, zoom: int, coord_x: float, coord_y: float, coord_z: float):
        world_to_map = map_obj['worldtomap']

        unscaled_x = world_to_map[0] * coord_x + world_to_map[1] * coord_y + world_to_map[2] * coord_z
        unscaled_y = world_to_map[3] * coord_x + world_to_map[4] * coord_y + world_to_map[5] * coord_z

        zoomed_scale = 2 ** zoom

        tile_x = DynmapCoords.floor(unscaled_x / DynmapCoords.scale_div, zoomed_scale)
        tile_y = DynmapCoords.ceil(-(128 - unscaled_y) / DynmapCoords.scale_div, zoomed_scale)

        return tile_x, tile_y

    @staticmethod
    def floor(num, zoomed_scale):
        return zoomed_scale * math.floor(num / zoomed_scale)

    @staticmethod
    def ceil(num, zoomed_scale):
        return zoomed_scale * math.ceil(num / zoomed_scale)
