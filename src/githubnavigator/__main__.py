"""Application main module."""

from .application import Application


def main() -> None:
    """Run application."""
    application = Application()
    application.config.from_yaml('config/config.yml')
    application.run_website()


if __name__ == '__main__':
    main()
