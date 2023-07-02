from models.config import Config
from core.state import State
from views.view import View


class Controller:
    def __init__(self, base_dir: str, config: Config, state: State, view: View):
        self.base_dir = base_dir
        self.config = config
        self.state = state
        self.view = view

    def build_view(self, parent):
        self.view.build_view(parent, self)
