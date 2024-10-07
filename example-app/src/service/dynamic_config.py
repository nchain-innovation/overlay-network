from typing import List, Any
import toml
import logging

from config import ConfigType


LOGGER = logging.getLogger(__name__)


class DynamicConfig:
    """ Class to read/write dynamic config
    """
    def __init__(self):
        self.filename = None
        self.config = {}

    def set_config(self, config: ConfigType):
        self.filename = config["dynamic_config"]["filename"]

    def add(self, fields: List[str], value: Any):

        pass

    def remove(self, fields: List[str], value: Any):
        pass

    def load(self):
        """ Load config from provided toml file
        """
        try:
            with open(self.filename, "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError as e:
            print(f"load_config - File not found error {e}")
            LOGGER.warning(f"load_config - File not found error {e}")
            self.config = {}



dynamic_config = DynamicConfig()
