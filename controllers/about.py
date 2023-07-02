import webbrowser

from controllers.controller import Controller


class AboutController(Controller):
    base_url = 'https://github.com/ryanbester/minecraft-map-tools'

    @staticmethod
    def open_github_link():
        webbrowser.open_new(AboutController.base_url)

    @staticmethod
    def open_issues_link():
        webbrowser.open_new('{}/issues'.format(AboutController.base_url))
