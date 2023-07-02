import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk, filedialog

from controllers.download import DownloadController, DownloadMcCoordsController, DownloadGridRefController, \
    DownloadDynmapTileController
from core.dynmap import Dynmap
from views.view import View


class DownloadMcCoordsFrame(View):
    controller: DownloadMcCoordsController
    from_x_txt: ttk.Entry
    from_y_txt: ttk.Entry
    from_z_txt: ttk.Entry
    to_x_txt: ttk.Entry
    to_y_txt: ttk.Entry
    to_z_txt: ttk.Entry
    zoom_txt: ttk.Entry

    def __init__(self):
        super().__init__()
        self.frame = None

    def build_view(self, parent, controller: DownloadMcCoordsController):
        self.controller = controller

        # Create the view if it's being shown for the first time
        if self.frame is None:
            self.frame = ttk.Frame(parent)

            self.frame.columnconfigure(index=0, weight=1)
            self.frame.columnconfigure(index=1, weight=1)
            self.frame.columnconfigure(index=2, weight=1)

            from_lbl = ttk.Label(self.frame, text='From: ')
            from_lbl.grid(row=0, column=0, padx=7, pady=7, columnspan=3)

            self.from_x_txt = ttk.Entry(self.frame)
            self.from_x_txt.grid(row=1, column=0, padx=7, pady=7, sticky='we')

            self.from_y_txt = ttk.Entry(self.frame)
            self.from_y_txt.grid(row=1, column=1, padx=7, pady=7, sticky='we')

            self.from_z_txt = ttk.Entry(self.frame)
            self.from_z_txt.grid(row=1, column=2, padx=7, pady=7, sticky='we')

            to_lbl = ttk.Label(self.frame, text='To: ')
            to_lbl.grid(row=2, column=0, padx=7, pady=7, columnspan=3)

            self.to_x_txt = ttk.Entry(self.frame)
            self.to_x_txt.grid(row=3, column=0, padx=7, pady=7, sticky='we')

            self.to_y_txt = ttk.Entry(self.frame)
            self.to_y_txt.grid(row=3, column=1, padx=7, pady=7, sticky='we')

            self.to_z_txt = ttk.Entry(self.frame)
            self.to_z_txt.grid(row=3, column=2, padx=7, pady=7, sticky='we')

            zoom_lbl = ttk.Label(self.frame, text='Zoom:')
            zoom_lbl.grid(row=4, column=0, padx=7, pady=7)

            self.zoom_txt = ttk.Entry(self.frame)
            self.zoom_txt.grid(row=4, column=1, padx=7, pady=7, sticky='we')
            self.zoom_txt.insert(0, '0')

        self.frame.grid(row=2, column=0, columnspan=3, padx=0, pady=0, sticky='nsew')

    def hide_view(self):
        if self.frame is not None:
            self.frame.grid_forget()

    def get_input(self) -> dict:
        coords_input = {}

        try:
            coords_input['from_x'] = float(self.from_x_txt.get())
        except ValueError:
            raise ValueError('From X Coordinate must be a float')

        try:
            coords_input['from_y'] = float(self.from_y_txt.get())
        except ValueError:
            raise ValueError('From Y Coordinate must be a float')

        try:
            coords_input['from_z'] = float(self.from_z_txt.get())
        except ValueError:
            raise ValueError('From Z Coordinate must be a float')

        try:
            coords_input['to_x'] = float(self.to_x_txt.get())
        except ValueError:
            raise ValueError('To X Coordinate must be a float')

        try:
            coords_input['to_y'] = float(self.to_y_txt.get())
        except ValueError:
            raise ValueError('To Y Coordinate must be a float')

        try:
            coords_input['to_z'] = float(self.to_z_txt.get())
        except ValueError:
            raise ValueError('To Z Coordinate must be a float')

        try:
            coords_input['zoom'] = int(self.zoom_txt.get())
        except ValueError:
            raise ValueError('Zoom must be an integer')

        return coords_input


class DownloadGridRefFrame(View):
    controller: DownloadGridRefController

    def __init__(self):
        super().__init__()
        self.frame = None

    def build_view(self, parent, controller: DownloadGridRefController):
        self.controller = controller

    def hide_view(self):
        if self.frame is not None:
            self.frame.grid_forget()

    def get_input(self) -> dict:
        return {}


class DownloadDynmapTileFrame(View):
    controller: DownloadDynmapTileController

    def __init__(self):
        super().__init__()
        self.frame = None

    def build_view(self, parent, controller: DownloadDynmapTileController):
        self.controller = controller

    def hide_view(self):
        if self.frame is not None:
            self.frame.grid_forget()

    def get_input(self) -> dict:
        return {}


class DownloadFrame(View):
    controller: DownloadController
    frame: ttk.LabelFrame
    coord_mode: tk.StringVar
    source: tk.StringVar
    map_id: tk.StringVar

    def __init__(self):
        super().__init__()
        self.source_dropdown = None
        self.map_type_dropdown = None
        self.coord_mode_frame = None

        self.output_dir_txt = None
        self.progress_bar = None
        self.progress_lbl = None

    def build_view(self, parent, controller: DownloadController):
        self.controller = controller

        self.frame = ttk.LabelFrame(parent, text='Download')
        self.frame.pack(fill='both', padx=7, pady=7, expand=True)

        self.frame.columnconfigure(index=0, weight=1)
        self.frame.columnconfigure(index=1, weight=1)
        self.frame.columnconfigure(index=2, weight=1)

        self.coord_mode = tk.StringVar()
        self.source = tk.StringVar()
        self.map_id = tk.StringVar()

        coord_mode_mc = ttk.Radiobutton(self.frame, text='Minecraft Coords', variable=self.coord_mode, value='mc',
                                        command=self.update_mode)
        coord_mode_mc.grid(row=0, column=0, padx=7, pady=7)

        coord_mode_grid = ttk.Radiobutton(self.frame, text='Grid Reference', variable=self.coord_mode, value='grid',
                                          command=self.update_mode)
        coord_mode_grid.grid(row=0, column=1, padx=7, pady=7)

        coord_mode_dynmap = ttk.Radiobutton(self.frame, text='Dynmap Tile', variable=self.coord_mode, value='dynmap',
                                            command=self.update_mode)
        coord_mode_dynmap.grid(row=0, column=2, padx=7, pady=7)

        self.update_source_dropdown()
        self.update_map_types_dropdown()

        output_dir_lbl = ttk.Label(self.frame, text='Output Directory')
        output_dir_lbl.grid(row=3, column=0, padx=7, pady=7, columnspan=3)

        self.output_dir_txt = ttk.Entry(self.frame)
        self.output_dir_txt.insert(0, os.getcwd())
        self.output_dir_txt.grid(row=4, column=0, padx=7, pady=7, columnspan=2, sticky='we')

        output_dir_browse_btn = ttk.Button(self.frame, text='Browse...', command=self.select_dir)
        output_dir_browse_btn.grid(row=4, column=2, padx=7, pady=7, sticky='we')

        download_btn = ttk.Button(self.frame, text='Download', command=self.controller.start_download)
        download_btn.grid(row=5, column=0, padx=7, pady=7)

        self.progress_lbl = ttk.Label(self.frame, text='Idle')
        self.progress_lbl.grid(row=6, column=0, padx=6, pady=7)

        self.progress_bar = ttk.Progressbar(self.frame)
        self.progress_bar.grid(row=6, column=1, padx=7, pady=7, columnspan=2, sticky='we')

    def select_dir(self):
        initial_dir = self.output_dir_txt.get()
        if len(initial_dir) < 1:
            initial_dir = os.getcwd()

        directory = filedialog.askdirectory(initialdir=initial_dir, title='Select output directory')
        if len(directory) > 0:
            self.output_dir_txt.delete(0, tk.END)
            self.output_dir_txt.insert(0, directory)

    def server_change(self):
        # Make sure view is created first
        if self.source_dropdown is not None and self.map_type_dropdown is not None:
            self.update_source_dropdown()
            self.update_map_types_dropdown()

    def update_source_dropdown(self):
        if self.source_dropdown is not None:
            self.source_dropdown.destroy()

        sources = []
        if self.controller.state.selected_server is not None:
            if len(self.controller.state.selected_server.dynmap_url) > 0:
                sources.append('Dynmap')
            if len(self.controller.state.selected_server.journeymap_url) > 0:
                sources.append('JourneyMap')

        default = None
        if len(sources) > 0:
            default = sources[0]

        self.source_dropdown = ttk.OptionMenu(self.frame, self.source, default, *sources, command=self.update_source)
        self.source_dropdown.grid(row=1, column=0, padx=7, pady=7)

    def update_map_types_dropdown(self):
        if self.map_type_dropdown is not None:
            self.map_type_dropdown.destroy()

        map_ids = []
        # noinspection PyBroadException
        try:
            if self.source.get() == 'Dynmap':
                dynmap_config = Dynmap.get_config(self.controller.state.selected_server)
                map_ids = Dynmap.get_map_ids(dynmap_config)
            elif self.source.get() == 'JourneyMap':
                map_ids = ['day', 'night', 'biome', 'topo']
        except ValueError as e:
            self.display_error(str(e))
            map_ids = []
        except Exception:
            self.display_error('Failed to get Dynmap configuration')
            map_ids = []

        default = None
        if len(map_ids) > 0:
            default = map_ids[0]

        self.map_type_dropdown = ttk.OptionMenu(self.frame, self.map_id, default, *map_ids)
        self.map_type_dropdown.grid(row=1, column=1, padx=7, pady=7)

    def update_source(self, _):
        self.update_map_types_dropdown()

    def update_mode(self):
        if self.coord_mode_frame is not None:
            self.coord_mode_frame.view.hide_view()

        mode = self.coord_mode.get()
        if mode == 'mc':
            self.coord_mode_frame = self.controller.mc_coords_controller
        elif mode == 'grid':
            self.coord_mode_frame = self.controller.grid_ref_controller
        elif mode == 'dynmap':
            self.coord_mode_frame = self.controller.dynmap_tile_controller

        self.coord_mode_frame.build_view(self.frame)

    def get_input(self) -> dict:
        user_input = {'source': self.source.get(), 'map_id': self.map_id.get(), 'output_dir': self.output_dir_txt.get(),
                      'coord_mode': self.coord_mode.get()}

        if len(user_input['output_dir']) < 1:
            raise ValueError('Output directory is not specified')

        if self.coord_mode_frame is None or len(user_input['coord_mode']) < 1:
            raise ValueError('Coordinate mode is not specified')

        user_input['range'] = self.coord_mode_frame.view.get_input()

        return user_input

    def poll_progress(self):
        self.progress_bar.config(mode='determinate')
        self.progress_bar.config(value=self.controller.progress)
        self.progress_lbl.config(text=self.controller.progress_msg)
        if self.controller.progress_msg != 'Idle':
            self.progress_bar.after(100, self.poll_progress)

    def display_error(self, message: str):
        tkinter.messagebox.showerror(self.controller.state.main_win.title(), message)
