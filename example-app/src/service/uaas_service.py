
import requests
import logging
from pydantic import BaseModel
from typing import Any, Dict
from config import ConfigType


LOGGER = logging.getLogger(__name__)
# UAAS_TIMEOUT = 4.0
UAAS_TIMEOUT = 10.0


class UaaSServiceException(Exception):
    pass


# This represents an address or locking script monitor
class Monitor(BaseModel):
    name: str
    track_descendants: bool
    address: None | str
    locking_script_pattern: None | str


# This represents a UTXO as a Service - Address Monitor
# Simplified for the App
class AddressMonitor(BaseModel):
    name: str
    address: str


class UaaSService:
    """ This class represents the UaaS interface
    """
    def __init__(self):
        self.service_url: str

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.service_url = config["uaas"]["url"]

    def get_status(self) -> Dict[str, Any]:
        """ Return the status of the uaas service
        """
        try:
            response = requests.get(self.service_url + "/status", timeout=UAAS_TIMEOUT)
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the UaaS is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")
        return data

    # UaaS
    def add_monitor(self, monitor: AddressMonitor) -> Dict[str, Any]:
        request_monitor = {"name": monitor.name, "track_descendants": True, "address": monitor.address, "locking_script_pattern": None}
        print(f'self.service_url + "/collection/monitor" = {self.service_url + "/collection/monitor"}')
        try:
            response = requests.post(self.service_url + "/collection/monitor", timeout=UAAS_TIMEOUT, json=request_monitor)
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the UaaS is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")
        return {
            "status": "Success",
        }

    def delete_monitor(self, monitor_name: str) -> Dict[str, Any]:
        """ This endpoint can delete an monitor with the provided address
        """
        delete_url = f"/collection/monitor?monitor_name={monitor_name}"
        try:
            response = requests.delete(self.service_url + delete_url, timeout=UAAS_TIMEOUT)
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the UaaS is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")
        return {
            "status": "Success",
        }
