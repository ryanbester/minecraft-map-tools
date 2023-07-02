import tkinter as tk
from typing import Optional, Callable

from models.server import Server


class State:
    main_win: tk.Wm
    selected_server: Optional[Server]
    server_change_callbacks: list[Callable]

    def __init__(self):
        pass

    def init_state(self, main_win: tk.Wm):
        self.main_win = main_win
        self.selected_server = None
        self.server_change_callbacks = []

    def register_server_change_callback(self, function: Callable):
        self.server_change_callbacks.append(function)

    def call_server_change_callbacks(self):
        for callback in self.server_change_callbacks:
            callback()
