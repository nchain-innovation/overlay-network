import requests
import logging
from pydantic import BaseModel
from typing import Any, Dict
from config import ConfigType
from tx_engine import Tx
from packaging.version import Version

LOGGER = logging.getLogger(__name__)


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
        self.required_version: str
        self.service_url: str
        self.timeout: float

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.required_version = config["uaas"]["required_version"]
        self.service_url = config["uaas"]["url"]
        self.timeout = config["uaas"]["timeout"]

    def get_status(self) -> Dict[str, Any]:
        """ Return the status of the uaas service
        """
        try:
            response = requests.get(self.service_url + "/status", timeout=self.timeout)
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

    def check_version(self):
        try:
            uaas_status = self.get_status()
        except UaaSServiceException:
            pass
        else:
            # Check version
            try:
                assert uaas_status is not None
                version = uaas_status["version"]
            except KeyError:
                print(f"uaas_status = {uaas_status}")
                raise UaaSServiceException("UTXO as a Service did not provide a version")
            else:
                if Version(version) < Version(self.required_version):
                    raise UaaSServiceException(f"UTXO as a Service needs to be version '{self.required_version}' or above.")

    # UaaS
    def add_monitor(self, monitor: AddressMonitor) -> Dict[str, Any]:
        request_monitor = {"name": monitor.name, "track_descendants": True, "address": monitor.address, "locking_script_pattern": None}
        print(f'self.service_url + "/collection/monitor" = {self.service_url + "/collection/monitor"}')
        try:
            response = requests.post(self.service_url + "/collection/monitor", timeout=self.timeout, json=request_monitor)
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
            response = requests.delete(self.service_url + delete_url, timeout=self.timeout)
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

    def broadcast_tx(self, tx: Tx) -> str:
        """ Broadcast the tx, return the tx.id if successful"""
        tx_str = tx.serialize().hex()
        print(f"tx_str = {tx_str}")
        request_tx = {"tx": tx_str}
        try:
            response = requests.post(self.service_url + "/tx/hex", timeout=self.timeout, json=request_tx)
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the UaaS is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
                return tx.id()
            else:
                LOGGER.debug(f"response = {response}")
                print("Failed to broadcast transaction.")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")

    def get_tx(self, txid: str) -> Dict[str, Any]:
        """ Given the txid return the tx as dictionary"""

        try:
            response = requests.get(self.service_url + f"/tx/hex?hash={txid}", timeout=self.timeout)
        except:
            raise UaaSServiceException("ConnectionError connecting to UaaS. Check that the UaaS is running.")
        match response.status_code:
            case 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
                return data
            case 422:
                return {"description": "Unable to find transaction"}
            case _:
                LOGGER.debug(f"response.status_code = {response.status_code}")
                LOGGER.debug(f"response = {response}")
                print("Unable to find transaction.")
                raise UaaSServiceException(f"ConnectionError connecting to UaaS. Response = {response}.")
