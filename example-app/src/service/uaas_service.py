
import requests
import logging

from typing import Any, Dict, Optional
from config import ConfigType


LOGGER = logging.getLogger(__name__)


class UaaSServiceException(Exception):
    pass


class UaaSService:
    """ This class represents the UaaS interface
    """
    def __init__(self):
        self.service_url: str

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.service_url = config["uaas"]["url"]

    def get_status(self) -> Optional[Dict[str, Any]]:
        """ Return the status of the uaas service
        """
        try:
            response = requests.get(self.service_url + "/status")
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the finance service is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")
        return data
