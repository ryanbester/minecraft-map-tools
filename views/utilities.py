import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from controllers.utilities import UtilitiesController, GridRefConvController, DynmapConvController
from core.dynmap import Dynmap
from views.view import View


class UtilitiesFrame(View):
    controller: UtilitiesController
    frame: ttk.LabelFrame

    def build_view(self, parent, controller: UtilitiesController):
        self.controller = controller

        self.frame = ttk.LabelFrame(parent, text='Utilities')
        self.frame.pack(fill='both', padx=7, pady=7, expand=True)

        grid_ref_conv_btn = ttk.Button(self.frame, text='Grid Reference Converter',
                                       command=self.controller.open_grid_ref_conv_dialog)
        grid_ref_conv_btn.pack(side=tk.LEFT, padx=7, pady=7)

        dynmap_conv_btn = ttk.Button(self.frame, text='Dynmap Converter',
                                     command=self.controller.open_dynmap_conv_dialog)
        dynmap_conv_btn.pack(side=tk.LEFT, padx=7, pady=7)


class GridRefConvDialog(View):
    controller: GridRefConvController
    dialog: tk.Toplevel
    mc_coords_x_txt: ttk.Entry
    mc_coords_z_txt: ttk.Entry
    grid_ref_txt: ttk.Entry
    url_lbl: ttk.Label

    def build_view(self, parent, controller: GridRefConvController):
        self.controller = controller

        self.dialog = tk.Toplevel()
        self.dialog.geometry('330x200')
        self.dialog.title('Grid Reference Converter')
        self.dialog.iconbitmap(os.path.join(os.path.dirname(__file__), '../icon.ico'))

        self.dialog.wait_visibility()
        self.dialog.grab_set()
        self.dialog.transient(self.controller.state.main_win)

        self.dialog.columnconfigure(index=0, weight=1)
        self.dialog.columnconfigure(index=1, weight=1)

        mc_coords_lbl = ttk.Label(self.dialog, text='Minecraft Region Coordinates: ')
        mc_coords_lbl.grid(row=0, column=0, padx=7, pady=7, columnspan=2)

        self.mc_coords_x_txt = ttk.Entry(self.dialog)
        self.mc_coords_x_txt.grid(row=1, column=0, padx=7, pady=7, sticky='ew')

        self.mc_coords_z_txt = ttk.Entry(self.dialog)
        self.mc_coords_z_txt.grid(row=1, column=1, padx=7, pady=7, sticky='ew')

        convert_to_mc_btn = ttk.Button(self.dialog, text='▲ To Minecraft', command=self.controller.to_mc)
        convert_to_mc_btn.grid(row=2, column=0, padx=7, pady=7)

        convert_to_grid_btn = ttk.Button(self.dialog, text='▼ To Grid Reference', command=self.controller.to_grid_ref)
        convert_to_grid_btn.grid(row=2, column=1, padx=7, pady=7)

        grid_ref_lbl = ttk.Label(self.dialog, text='Grid Reference: ')
        grid_ref_lbl.grid(row=3, column=0, padx=7, pady=7, columnspan=2)

        self.grid_ref_txt = ttk.Entry(self.dialog)
        self.grid_ref_txt.grid(row=4, column=0, padx=7, pady=7, sticky='ew', columnspan=2)

        self.dialog.mainloop()

    def get_mc_input(self) -> dict:
        mc_input = {}

        try:
            mc_input['coords_x'] = float(self.mc_coords_x_txt.get())
        except ValueError:
            raise ValueError('X Coordinate must be a float')

        try:
            mc_input['coords_z'] = float(self.mc_coords_z_txt.get())
        except ValueError:
            raise ValueError('Z Coordinate must be a float')

        return mc_input

    def get_grid_ref_input(self) -> str:
        return self.grid_ref_txt.get()

    def set_mc_output(self, coords_x: int, coords_z: int):
        self.mc_coords_x_txt.delete(0, tk.END)
        self.mc_coords_x_txt.insert(0, str(coords_x))
        self.mc_coords_z_txt.delete(0, tk.END)
        self.mc_coords_z_txt.insert(0, str(coords_z))

    def set_grid_ref_output(self, grid_ref: str):
        self.grid_ref_txt.delete(0, tk.END)
        self.grid_ref_txt.insert(0, grid_ref)

    def display_error(self, message: str):
        tkinter.messagebox.showerror(self.dialog.title(), message)


class DynmapConvDialog(View):
    controller: DynmapConvController
    dialog: tk.Toplevel
    zoom_txt: ttk.Entry
    mc_coords_x_txt: ttk.Entry
    mc_coords_y_txt: ttk.Entry
    mc_coords_z_txt: ttk.Entry
    tile_x_txt: ttk.Entry
    tile_y_txt: ttk.Entry
    url_lbl: ttk.Label

    def build_view(self, parent, controller: DynmapConvController):
        self.controller = controller

        self.dialog = tk.Toplevel()
        self.dialog.geometry('470x330')
        self.dialog.title('Dynmap Converter')
        self.dialog.iconbitmap(os.path.join(os.path.dirname(__file__), '../icon.ico'))

        self.dialog.wait_visibility()
        self.dialog.grab_set()
        self.dialog.transient(self.controller.state.main_win)

        self.dialog.columnconfigure(index=0, weight=1)
        self.dialog.columnconfigure(index=1, weight=1)
        self.dialog.columnconfigure(index=2, weight=1)

        # noinspection PyBroadException
        try:
            self.controller.dynmap_config = Dynmap.get_config(self.controller.state.selected_server)
            map_ids = Dynmap.get_map_ids(self.controller.dynmap_config)
        except ValueError as e:
            self.display_error(str(e))
            self.dialog.destroy()
            return
        except Exception:
            self.display_error('Failed to get Dynmap configuration')
            self.dialog.destroy()
            return

        self.controller.selected_map = tk.StringVar()
        map_dropdown = ttk.OptionMenu(self.dialog, self.controller.selected_map, map_ids[0], *map_ids)
        map_dropdown.grid(row=0, column=0, padx=7, pady=7, columnspan=3)

        zoom_lbl = ttk.Label(self.dialog, text='Zoom: ')
        zoom_lbl.grid(row=1, column=0, padx=7, pady=7, columnspan=3)

        self.zoom_txt = ttk.Entry(self.dialog)
        self.zoom_txt.insert(0, '0')
        self.zoom_txt.grid(row=2, column=1, padx=7, pady=7, sticky='ew')

        mc_coords_lbl = ttk.Label(self.dialog, text='Minecraft Coordinates: ')
        mc_coords_lbl.grid(row=3, column=0, padx=7, pady=7, columnspan=3)

        self.mc_coords_x_txt = ttk.Entry(self.dialog)
        self.mc_coords_x_txt.grid(row=4, column=0, padx=7, pady=7, sticky='ew')

        self.mc_coords_y_txt = ttk.Entry(self.dialog)
        self.mc_coords_y_txt.grid(row=4, column=1, padx=7, pady=7, sticky='ew')

        self.mc_coords_z_txt = ttk.Entry(self.dialog)
        self.mc_coords_z_txt.grid(row=4, column=2, padx=7, pady=7, sticky='ew')

        convert_to_tile_btn = ttk.Button(self.dialog, text='▼ To Tile', command=self.controller.to_tile)
        convert_to_tile_btn.grid(row=5, column=2, padx=7, pady=7)

        tile_lbl = ttk.Label(self.dialog, text='Tile Coordinates: ')
        tile_lbl.grid(row=6, column=0, padx=7, pady=7, columnspan=3)

        self.tile_x_txt = ttk.Entry(self.dialog)
        self.tile_x_txt.grid(row=7, column=0, padx=7, pady=7, sticky='ew')

        self.tile_y_txt = ttk.Entry(self.dialog)
        self.tile_y_txt.grid(row=7, column=1, padx=7, pady=7, sticky='ew')

        self.url_lbl = ttk.Label(self.dialog, text='URL will be displayed here')
        self.url_lbl.grid(row=8, column=0, padx=7, pady=7, columnspan=2, sticky='w')

        copy_url_btn = ttk.Button(self.dialog, text='Copy URL', command=self.copy_url)
        copy_url_btn.grid(row=8, column=2, padx=7, pady=7, sticky='e')

        self.dialog.mainloop()

    def get_input(self) -> dict:
        coord_input = {}

        try:
            coord_input['zoom'] = int(self.zoom_txt.get())
        except ValueError:
            raise ValueError('Zoom level must be an integer')

        try:
            coord_input['coords_x'] = float(self.mc_coords_x_txt.get())
        except ValueError:
            raise ValueError('X Coordinate must be a float')

        try:
            coord_input['coords_y'] = float(self.mc_coords_y_txt.get())
        except ValueError:
            raise ValueError('Y Coordinate must be a float')

        try:
            coord_input['coords_z'] = float(self.mc_coords_z_txt.get())
        except ValueError:
            raise ValueError('Z Coordinate must be a float')

        return coord_input

    def copy_url(self):
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(self.url_lbl.cget('text'))

    def set_output(self, tile_x: float, tile_y: float, url: str):
        self.tile_x_txt.delete(0, tk.END)
        self.tile_x_txt.insert(0, str(tile_x))
        self.tile_y_txt.delete(0, tk.END)
        self.tile_y_txt.insert(0, str(tile_y))
        self.url_lbl.config(text=url)

    def display_error(self, message: str):
        tkinter.messagebox.showerror(self.dialog.title(), message)
