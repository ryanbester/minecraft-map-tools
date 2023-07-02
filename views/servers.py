import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from controllers.servers import ServersController, EditServerController
from models.server import Server
from views.view import View


class ServersFrame(View):
    controller: ServersController
    frame: ttk.LabelFrame
    servers_dropdown: ttk.OptionMenu = None
    selected_server: tk.StringVar
    server_names = []

    def build_view(self, parent, controller: ServersController):
        self.controller = controller

        self.frame = ttk.LabelFrame(parent, text='Servers')
        self.frame.pack(fill='both', padx=7, pady=7, expand=True)

        self.selected_server = tk.StringVar()
        self.update_servers_dropdown(None)

        add_button = ttk.Button(self.frame, text='Add', command=self.controller.add_server)
        add_button.grid(row=1, column=0, padx=7, pady=7)

        edit_button = ttk.Button(self.frame, text='Edit', command=self.controller.edit_server)
        edit_button.grid(row=1, column=1, padx=7, pady=7)

        delete_button = ttk.Button(self.frame, text='Delete', command=self.controller.delete_server)
        delete_button.grid(row=1, column=2, padx=7, pady=7)

    def update_servers_dropdown(self, selected=None):
        if self.servers_dropdown is not None:
            self.servers_dropdown.destroy()

        self.populate_servers()

        if len(self.server_names) > 0:
            selected = self.server_names[0]
        elif len(self.selected_server.get()) != 0:
            selected = self.selected_server.get()

        self.controller.select_server(selected)

        self.servers_dropdown = ttk.OptionMenu(self.frame, self.selected_server, selected,
                                               *self.server_names, command=self.controller.select_server)
        self.servers_dropdown.grid(row=0, column=0, padx=7, pady=7, columnspan=3, sticky='w')

    def populate_servers(self):
        self.server_names.clear()

        for server in self.controller.config.servers:
            self.server_names.append(server.name)


class EditServerDialog(View):
    edit_server_win: tk.Toplevel
    name_txt: ttk.Entry
    dynmap_txt: ttk.Entry
    journeymap_txt: ttk.Entry
    ignore_ssl_cert: tk.IntVar

    def build_view(self, parent, controller: EditServerController):
        self.edit_server_win = tk.Toplevel()
        self.edit_server_win.geometry('300x220')
        self.edit_server_win.title(controller.title)
        self.edit_server_win.iconbitmap(os.path.join(os.path.dirname(__file__), '../icon.ico'))

        self.edit_server_win.wait_visibility()
        self.edit_server_win.grab_set()
        self.edit_server_win.transient(controller.state.main_win)

        self.edit_server_win.columnconfigure(index=0, weight=1)
        self.edit_server_win.columnconfigure(index=1, weight=1)

        name_lbl = ttk.Label(self.edit_server_win, text='Server Name: ')
        name_lbl.grid(row=0, column=0, padx=7, pady=7, sticky='e')

        self.name_txt = ttk.Entry(self.edit_server_win)
        self.name_txt.grid(row=0, column=1, padx=7, pady=7, sticky='ew')

        url_lbl = ttk.Label(self.edit_server_win, text='Leave the URL blank if it is not applicable')
        url_lbl.grid(row=1, column=0, padx=7, pady=7, columnspan=2)

        dynmap_lbl = ttk.Label(self.edit_server_win, text='Dynmap URL: ')
        dynmap_lbl.grid(row=2, column=0, padx=7, pady=7, sticky='e')

        self.dynmap_txt = ttk.Entry(self.edit_server_win)
        self.dynmap_txt.grid(row=2, column=1, padx=7, pady=7, sticky='ew')

        journeymap_lbl = ttk.Label(self.edit_server_win, text='JourneyMap URL: ')
        journeymap_lbl.grid(row=3, column=0, padx=7, pady=7, sticky='e')

        self.journeymap_txt = ttk.Entry(self.edit_server_win)
        self.journeymap_txt.grid(row=3, column=1, padx=7, pady=7, sticky='ew')

        self.ignore_ssl_cert = tk.IntVar()

        if controller.server is not None:
            self.name_txt.insert(0, controller.server.name)
            self.dynmap_txt.insert(0, controller.server.dynmap_url)
            self.journeymap_txt.insert(0, controller.server.journeymap_url)
            if controller.server.ignore_ssl_cert is True:
                self.ignore_ssl_cert.set(1)

        ignore_ssl_cert_check = ttk.Checkbutton(self.edit_server_win, text='Ignore SSL certificate validation',
                                                variable=self.ignore_ssl_cert)
        ignore_ssl_cert_check.grid(row=4, column=0, padx=7, pady=7, columnspan=2)

        cancel_btn = ttk.Button(self.edit_server_win, text='Cancel', command=self.edit_server_win.destroy)
        cancel_btn.grid(row=5, column=0, padx=7, pady=7, sticky='e')

        save_btn = ttk.Button(self.edit_server_win, text='Save', command=controller.save)
        save_btn.grid(row=5, column=1, padx=7, pady=7, sticky='w')

        self.edit_server_win.mainloop()

    def get_input(self) -> Server:
        name = self.name_txt.get()
        dynmap_url = self.dynmap_txt.get()
        journeymap_url = self.journeymap_txt.get()
        try:
            ignore_ssl_cert = bool(self.ignore_ssl_cert.get())
        except ValueError:
            raise ValueError('Ignore SSL Cert not valid')

        return Server(name, dynmap_url, journeymap_url, ignore_ssl_cert)

    def display_error(self, message: str):
        tkinter.messagebox.showerror(self.edit_server_win.title(), message)
