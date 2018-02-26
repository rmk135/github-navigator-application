"""GitHub Navigator application - config loader."""

import yaml


class ConfigLoader:
    """Config loader."""

    def __init__(self, path):
        """Initializer."""
        self._path = path

    def load(self):
        """Load config data from file."""
        try:
            with open(self._path) as config_file:
                config_data = yaml.load(config_file)
        except IOError:
            config_data = {}
        finally:
            return config_data
