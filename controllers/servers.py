import tkinter.messagebox
from typing import Callable

import validators

from controllers.configprovider import ConfigProvider
from controllers.controller import Controller
from core.state import State
from models.config import Config
from models.server import Server
from views.view import View


class EditServerController(Controller):
    update_servers_dropdown: Callable
    title: str
    server: Server

    def __init__(self, base_dir: str, config: Config, state: State, view: View, config_provider: ConfigProvider):
        super().__init__(base_dir, config, state, view)
        self.config_provider = config_provider

    def build_view(self, parent, update_servers_dropdown: Callable = None, title='Edit Server', server: Server = None):
        self.update_servers_dropdown = update_servers_dropdown
        self.title = title
        self.server = server
        super().build_view(parent)

    def save(self):
        try:
            input_server: Server = self.view.get_input()
        except ValueError as e:
            self.view.display_error(str(e))
            return

        if len(input_server.name) < 1:
            self.view.display_error('Server name cannot be blank')
            return

        if len(input_server.dynmap_url) > 0 and validators.url(input_server.dynmap_url) is not True:
            self.view.display_error('Dynmap URL is not valid')
            return

        if len(input_server.journeymap_url) > 0 and validators.url(input_server.journeymap_url) is not True:
            self.view.display_error('JourneyMap URL is not valid')
            return

        if self.server is not None:
            # Edit existing
            to_update = None
            for config_server in self.config.servers:
                if config_server.name == self.server.name:
                    to_update = config_server

            if to_update is not None:
                to_update.name = input_server.name
                to_update.dynmap_url = input_server.dynmap_url
                to_update.journeymap_url = input_server.journeymap_url
                to_update.ignore_ssl_cert = input_server.ignore_ssl_cert
        else:
            # Add new
            self.config.servers.append(input_server)

        try:
            self.config_provider.save_config()
        except (OSError, ValueError):
            self.view.display_error('Failed to save server details')
            return

        if self.update_servers_dropdown is not None:
            self.update_servers_dropdown()

        self.state.call_server_change_callbacks()

        self.view.edit_server_win.destroy()


class ServersController(Controller):
    def __init__(self, base_dir: str, config: Config, state: State, view: View, config_provider: ConfigProvider,
                 edit_server_controller: EditServerController):
        super().__init__(base_dir, config, state, view)
        self.config_provider = config_provider
        self.edit_server_controller = edit_server_controller

    def select_server(self, server_name):
        for config_server in self.config.servers:
            if config_server.name == server_name:
                self.state.selected_server = config_server
        self.state.call_server_change_callbacks()

    def add_server(self):
        self.edit_server_controller.build_view(self.state.main_win, self.view.update_servers_dropdown, 'Add server')

    def edit_server(self):
        self.edit_server_controller.build_view(self.state.main_win, self.view.update_servers_dropdown,
                                               server=self.state.selected_server)

    def delete_server(self):
        for config_server in self.config.servers:
            if config_server.name == self.state.selected_server.name:
                self.config.servers.remove(config_server)

        try:
            self.config_provider.save_config()
        except (OSError, ValueError):
            tkinter.messagebox.showerror(self.state.main_win.title(), 'Failed to save servers')
            return

        self.view.update_servers_dropdown()
        self.state.call_server_change_callbacks()
