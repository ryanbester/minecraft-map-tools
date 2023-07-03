import os.path
from threading import Thread
from typing import Optional

from controllers.controller import Controller
from core.dynmap import Dynmap
from core.dynmapcoords import DynmapCoords
from core.gridref import GridRef
from core.map import Map
from core.state import State
from models.config import Config
from views.view import View


class DownloadMcCoordsController(Controller):
    pass


class DownloadGridRefController(Controller):
    pass


class DownloadDynmapTileController(Controller):
    pass


class DownloadController(Controller):
    progress: int
    progress_msg: str
    download_thread: Optional[Thread]

    def __init__(self, base_dir: str, config: Config, state: State, view: View,
                 mc_coords_controller: DownloadMcCoordsController,
                 grid_ref_controller: DownloadGridRefController,
                 dynmap_tile_controller: DownloadDynmapTileController):
        super().__init__(base_dir, config, state, view)
        self.mc_coords_controller = mc_coords_controller
        self.grid_ref_controller = grid_ref_controller
        self.dynmap_tile_controller = dynmap_tile_controller

        self.download_thread = None

    def server_change(self):
        self.view.server_change()

    def start_download(self):
        self.progress_msg = ''
        self.progress = 0
        self.download_thread = Thread(target=self.download)
        self.download_thread.start()
        self.view.poll_progress()

    # noinspection PyBroadException
    def download(self):
        try:
            user_input = self.view.get_input()
        except ValueError as e:
            self.view.display_error(str(e))
            return

        tiles_dir = os.path.join(user_input['output_dir'], 'tiles')

        try:
            if not os.path.isdir(tiles_dir):
                os.makedirs(tiles_dir)
        except OSError:
            self.view.display_error('Failed to create tiles directory')
            return

        input_range = user_input['range']

        if user_input['source'] == 'Dynmap':
            dynmap_config = Dynmap.get_config(self.state.selected_server)
            map_obj = Dynmap.get_map_obj(dynmap_config, user_input['map_id'])

            if user_input['coord_mode'] == 'mc':
                from_tile_x, from_tile_y = DynmapCoords.mc_to_tile(map_obj, input_range['zoom'],
                                                                   input_range['from_x'], input_range['from_y'],
                                                                   input_range['from_z']
                                                                   )
                to_tile_x, to_tile_y = DynmapCoords.mc_to_tile(map_obj, input_range['zoom'],
                                                               input_range['to_x'], input_range['to_y'],
                                                               input_range['to_z']
                                                               )
            elif user_input['coord_mode'] == 'grid':
                try:
                    from_region_x, from_region_y = GridRef.grid_ref_to_mc(input_range['from'])
                except ValueError as e:
                    self.view.display_error('From grid reference: {}'.format(str(e)))
                    return

                try:
                    to_region_x, to_region_y = GridRef.grid_ref_to_mc(input_range['to'])
                except ValueError as e:
                    self.view.display_error('To grid reference: {}'.format(str(e)))
                    return

                low_region_x = min(from_region_x, to_region_x)
                low_region_y = min(from_region_y, to_region_y)
                high_region_x = max(from_region_x, to_region_x)
                high_region_y = max(from_region_y, to_region_y)

                from_x = (low_region_x << 5) << 4
                from_y = (low_region_y << 5) << 4
                to_x = (((high_region_x + 1 << 5) - 1) + 1 << 4) - 1
                to_y = (((high_region_y + 1 << 5) - 1) + 1 << 4) - 1

                from_tile_x, from_tile_y = DynmapCoords.mc_to_tile(map_obj, input_range['zoom'], from_x, 64, from_y)
                to_tile_x, to_tile_y = DynmapCoords.mc_to_tile(map_obj, input_range['zoom'], to_x, 64, to_y)
            elif user_input['coord_mode'] == 'dynmap':
                from_tile_x = input_range['from_x']
                from_tile_y = input_range['from_y']
                to_tile_x = input_range['to_x']
                to_tile_y = input_range['to_y']
            else:
                self.view.display_error('Invalid coordinate mode')
                return

            low_tile_x = min(from_tile_x, to_tile_x)
            low_tile_y = min(from_tile_y, to_tile_y)
            high_tile_x = max(from_tile_x, to_tile_x)
            high_tile_y = max(from_tile_y, to_tile_y)

            map_id = user_input['map_id'].split(' - ')
            world_name, map_name = map_id[0], map_id[1]

            try:
                stitch_args = Dynmap.download_tiles(tiles_dir, self.state.selected_server.dynmap_url, world_name,
                                                    map_name,
                                                    input_range['zoom'], low_tile_x, low_tile_y,
                                                    high_tile_x, high_tile_y, self.update_progress)
            except Exception:
                self.view.display_error('Failed to download tiles')
                return

            try:
                Map.stitch(tiles_dir, user_input['output_dir'], stitch_args, self.update_progress)
            except Exception:
                self.view.display_error('Failed to stitch tiles')
                return

            self.update_progress('Idle', 0, 1)

    def update_progress(self, message: str, i, total):
        self.progress_msg = message
        self.progress = int((i / total) * 100)
