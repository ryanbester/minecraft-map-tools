import os
import tkinter as tk
from tkinter import ttk

from controllers.main import MainController
from views.view import View


class MainView(View):
    def build_view(self, parent, controller: MainController):
        main_win = tk.Tk()
        main_win.title('Minecraft Map Tools')
        main_win.geometry('900x700')

        main_win.columnconfigure(0, weight=2)
        main_win.columnconfigure(1, weight=1)

        controller.state.init_state(main_win)
        controller.state.register_server_change_callback(controller.download_controller.server_change)

        left_frame = ttk.Frame(main_win)
        left_frame.grid(row=0, column=0, sticky='new')

        right_frame = ttk.Frame(main_win)
        right_frame.grid(row=0, column=1, sticky='new')

        controller.servers_controller.build_view(left_frame)
        controller.download_controller.build_view(left_frame)
        controller.utilities_controller.build_view(right_frame)
        controller.about_controller.build_view(right_frame)

        main_win.iconbitmap(os.path.join(controller.base_dir, 'icon.ico'))
        main_win.mainloop()
