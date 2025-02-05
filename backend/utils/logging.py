
import logging

from utils.types_scraper import SingletonMeta
from utils.config_parser import ConfigParser

class ScraperLogger(metaclass=SingletonMeta):
    """
    # Singleton Logger to log either to stream or file
    """
    LOGGER_SECTION = 'logger'

    def __init__(self, name='scraper_logger', log_file='scraper.log', config= ConfigParser()):
        """
        # Inits a logger
        """
        name = config.get('logger', 'name', default=name)
        self.logger = logging.getLogger(name)
        _level = config.get('logger', 'log_level', default='INFO')
        self.logger.setLevel(_level)

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.console_handler.setFormatter(self.formatter)

        log_file = config.get('logger', 'log_file', default=log_file)
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    def get_logger(self):
        """
        # Returns a logger object
        """
        return self.logger

logger = ScraperLogger().get_logger()

