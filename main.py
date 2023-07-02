from core.container import Application


def main():
    container = Application()

    try:
        container.core.config_provider().read_config()
        container.core.config_provider().save_config()
    except OSError as e:
        print('Failed to load config: ' + str(e))
        exit(1)

    container.controllers.main_controller().build_view(None)


if __name__ == '__main__':
    main()
