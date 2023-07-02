import tkinter as tk

from controllers.controller import Controller
from core.dynmap import Dynmap
from core.gridref import GridRef
from core.state import State
from core.dynmapcoords import DynmapCoords
from models.config import Config
from views.view import View


class GridRefConvController(Controller):
    def to_mc(self):
        grid_ref = self.view.get_grid_ref_input()

        try:
            region_x, region_z = GridRef.grid_ref_to_mc(grid_ref)
            self.view.set_mc_output(int(region_x), int(region_z))
        except ValueError as e:
            self.view.display_error(str(e))

    def to_grid_ref(self):
        try:
            mc_input = self.view.get_mc_input()
        except ValueError as e:
            self.view.display_error(str(e))
            return

        try:
            grid_ref = GridRef.mc_to_grid_ref(mc_input['coords_x'], mc_input['coords_z'])
            self.view.set_grid_ref_output(grid_ref)
        except ValueError as e:
            self.view.display_error(str(e))
            return


class DynmapConvController(Controller):
    selected_map: tk.StringVar
    dynmap_config: dict

    def to_tile(self):
        try:
            map_obj = Dynmap.get_map_obj(self.dynmap_config, self.selected_map.get())
        except KeyError:
            self.view.display_error('Invalid map')
            return

        if map_obj is None:
            self.view.display_error('Map not found')
            return

        try:
            coord_input = self.view.get_input()
        except ValueError as e:
            self.view.display_error(str(e))
            return

        try:
            tile_x, tile_y = DynmapCoords.mc_to_tile(map_obj,
                                                     coord_input['zoom'], coord_input['coords_x'],
                                                     coord_input['coords_y'], coord_input['coords_z']
                                                     )

            map_id = self.selected_map.get().split(' - ')
            world_name, map_name = map_id[0], map_id[1]

            tile_path = Dynmap.get_tile_path(world_name, map_name, coord_input['zoom'], tile_x, tile_y)
            url = self.state.selected_server.dynmap_url + tile_path

            self.view.set_output(tile_x, tile_y, url)
        except ValueError:
            self.view.display_error('Cannot convert coordinates')


class UtilitiesController(Controller):
    def __init__(self, base_dir: str, config: Config, state: State, view: View,
                 grid_ref_conv_controller: GridRefConvController,
                 dynmap_conv_controller: DynmapConvController):
        super().__init__(base_dir, config, state, view)
        self.grid_ref_conv_controller = grid_ref_conv_controller
        self.dynmap_conv_controller = dynmap_conv_controller

    def open_grid_ref_conv_dialog(self):
        self.grid_ref_conv_controller.build_view(self.view.frame)

    def open_dynmap_conv_dialog(self):
        self.dynmap_conv_controller.build_view(self.view.frame)
