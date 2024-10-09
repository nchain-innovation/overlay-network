from typing import Any
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
        self.load()

    def __getitem__(self, field: str) -> Any:
        # print(f"self.config = {self.config}")
        return self.config[field]

    def __contains__(self, field: str) -> bool:
        return field in self.config

    def __setitem__(self, field: str, value: Any):
        LOGGER.info(f"DynamicConfig - Add field {field}")
        self.config[field] = value
        self.save()

    def __delitem__(self, field: str):
        LOGGER.info(f"DynamicConfig - Remove field {field}")
        del self.config[field]
        self.save()

    def load(self):
        """ Load config from provided toml file
        """
        assert self.filename is not None
        try:
            with open(self.filename, "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            # print(f"DynamicConfig - File not found error {e}")
            # LOGGER.warning(f"DynamicConfig - File not found error {e}")
            self.config = {}

    def save(self):
        assert self.filename is not None
        with open(self.filename, "w") as f:
            toml.dump(self.config, f)


dynamic_config = DynamicConfig()
