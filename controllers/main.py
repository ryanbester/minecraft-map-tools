from controllers.about import AboutController
from controllers.controller import Controller
from controllers.download import DownloadController
from controllers.servers import ServersController
from controllers.utilities import UtilitiesController
from core.state import State
from models.config import Config
from views.view import View


class MainController(Controller):
    def __init__(self, base_dir: str, config: Config, state: State, view: View, servers_controller: ServersController,
                 download_controller: DownloadController, utilities_controller: UtilitiesController,
                 about_controller: AboutController):
        super().__init__(base_dir, config, state, view)

        self.servers_controller = servers_controller
        self.download_controller = download_controller
        self.utilities_controller = utilities_controller
        self.about_controller = about_controller
