import json
import os

from utils.constants import GenericConstants as generic_constants
from utils.types_scraper import SingletonMeta

class ConfigParser(metaclass=SingletonMeta):

    def __init__(self, config_file_path=None):
        self.config_file = self._get_config_path(config_file_path)
        self.config = self.load_config()

    @staticmethod
    def _get_config_path(config_file_path: str):
        if config_file_path:
            joined_path = os.path.join(generic_constants.PROJECT_ROOT_LOCATION.value, config_file_path)
        else:
            joined_path = os.path.join(generic_constants.PROJECT_ROOT_LOCATION.value, generic_constants.DEFAULT_CONFIG_LOCATION.value)
        return joined_path

    @staticmethod
    def update_config_from_env(config):
        """
            Updates fields for ex username and password using
            format from env vars SECTION1_SECTION2__FIELD
        """
        pattern = r"^([A-Za-z0-9_]+(?:__[A-Za-z0-9_]+)*)__(\w+)$"
        import re
        regex = re.compile(pattern)
        for key, value in os.environ.items():
            match = regex.match(key)
            if match:
                sections = match.group(1).split('__')
                field = match.group(2).lower()
                current_dict = config
                for section in sections:
                    current_dict = current_dict.get(section.lower(), {})
                current_dict[field] = value

                print(f"Updated {key} with value: {value}")
        return config


    def load_config(self):
        config = self.read_file()
        config = self.update_config_from_env(config)
        return config

    def read_file(self):
        data = {}
        try:
            with open(self.config_file, 'r') as config:
                data = json.load(config)
                print("Successfully loaded the data")
        except (json.JSONDecodeError, FileNotFoundError, IOError) as ex:
            print("Exception reading error")
            raise ex
        return data

    def get(self, *keys, default=None):
        try:
            value = self.config
            for key in keys:
                value = value.get(key, default) if isinstance(value, dict) else default
            return value
        except TypeError:
            return default

    def to_json(self):
        return self.config