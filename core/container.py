import os

import appdirs
from dependency_injector import containers
from dependency_injector import providers

from views.main import MainView
from views.servers import ServersFrame, EditServerDialog
from views.download import DownloadFrame, DownloadMcCoordsFrame, DownloadGridRefFrame, DownloadDynmapTileFrame
from views.utilities import UtilitiesFrame, GridRefConvDialog, DynmapConvDialog
from views.about import AboutFrame

from core.state import State
from models.config import Config

from controllers.configprovider import ConfigProvider
from controllers.main import MainController
from controllers.servers import ServersController, EditServerController
from controllers.download import DownloadController, DownloadMcCoordsController, DownloadGridRefController, \
    DownloadDynmapTileController
from controllers.utilities import UtilitiesController, GridRefConvController, DynmapConvController
from controllers.about import AboutController


class Core(containers.DeclarativeContainer):
    base_dir = providers.Object(os.path.join(os.path.dirname(__file__), '..'))

    config_dir = providers.Object(appdirs.user_config_dir('MinecraftMapTools', 'Bester', roaming=True))

    config = providers.Singleton(Config)
    config_provider = providers.Singleton(
        ConfigProvider,
        config, config_dir, 'config.json'
    )

    state = providers.Singleton(State)


class Views(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()

    servers_frame = providers.Singleton(ServersFrame)
    edit_server_dialog = providers.Singleton(EditServerDialog)

    download_frame = providers.Singleton(DownloadFrame)
    download_mc_coords_frame = providers.Singleton(DownloadMcCoordsFrame)
    download_grid_ref_frame = providers.Singleton(DownloadGridRefFrame)
    download_dynmap_tile_frame = providers.Singleton(DownloadDynmapTileFrame)

    utilities_frame = providers.Singleton(UtilitiesFrame)
    grid_ref_conv_dialog = providers.Singleton(GridRefConvDialog)
    dynmap_conv_dialog = providers.Singleton(DynmapConvDialog)

    about_frame = providers.Singleton(AboutFrame)

    main_view = providers.Singleton(MainView)


class Controllers(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()
    views = providers.DependenciesContainer()

    edit_server_controller = providers.Singleton(
        EditServerController,
        core.base_dir,
        core.config,
        core.state,
        views.edit_server_dialog,
        core.config_provider
    )
    servers_controller = providers.Singleton(
        ServersController,
        core.base_dir,
        core.config,
        core.state,
        views.servers_frame,
        core.config_provider,
        edit_server_controller
    )

    download_mc_coords_controller = providers.Singleton(
        DownloadMcCoordsController,
        core.base_dir,
        core.config,
        core.state,
        views.download_mc_coords_frame
    )
    download_grid_ref_controller = providers.Singleton(
        DownloadGridRefController,
        core.base_dir,
        core.config,
        core.state,
        views.download_grid_ref_frame
    )
    download_dynmap_tile_controller = providers.Singleton(
        DownloadDynmapTileController,
        core.base_dir,
        core.config,
        core.state,
        views.download_dynmap_tile_frame
    )
    download_controller = providers.Singleton(
        DownloadController,
        core.base_dir,
        core.config,
        core.state,
        views.download_frame,
        download_mc_coords_controller,
        download_grid_ref_controller,
        download_dynmap_tile_controller
    )

    grid_ref_conv_controller = providers.Singleton(
        GridRefConvController,
        core.base_dir,
        core.config,
        core.state,
        views.grid_ref_conv_dialog
    )
    dynmap_conv_controller = providers.Singleton(
        DynmapConvController,
        core.base_dir,
        core.config,
        core.state,
        views.dynmap_conv_dialog
    )
    utilities_controller = providers.Singleton(
        UtilitiesController,
        core.base_dir,
        core.config,
        core.state,
        views.utilities_frame,
        grid_ref_conv_controller,
        dynmap_conv_controller
    )

    about_controller = providers.Singleton(
        AboutController,
        core.base_dir,
        core.config,
        core.state,
        views.about_frame
    )

    main_controller = providers.Singleton(
        MainController,
        core.base_dir,
        core.config,
        core.state,
        views.main_view,
        servers_controller,
        download_controller,
        utilities_controller,
        about_controller
    )


class Application(containers.DeclarativeContainer):
    core = providers.Container(Core)
    views = providers.Container(Views, core=core)
    controllers = providers.Container(Controllers, core=core, views=views)
