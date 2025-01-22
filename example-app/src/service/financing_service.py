import requests
import logging
import json
from typing import Any, Dict, Optional
from config import ConfigType
from packaging.version import Version

LOGGER = logging.getLogger(__name__)


class FinancingServiceException(Exception):
    pass


class FinancingService:
    """ This class represents the Financing Service interface
    """
    def __init__(self):
        self.required_version: str
        self.service_url: str
        self.timeout: float
        self.utxo_cache_enabled: bool
        self.utxo_persistence_enabled: bool
        self.utxo_file: str
        self.utxo_min_level: int
        self.utxo_request_level: int
        self.utxo = {}

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.required_version = config["finance_service"]["required_version"]
        self.service_url = config["finance_service"]["url"]
        self.timeout = config["finance_service"]["timeout"]
        # cache stuff
        self.utxo_cache_enabled = config["finance_service"]["utxo_cache_enabled"]
        self.utxo_persistence_enabled = config["finance_service"]["utxo_persistence_enabled"]
        self.utxo_file = config["finance_service"]["utxo_file"]
        self.utxo_min_level = config["finance_service"]["utxo_min_level"]
        self.utxo_request_level = config["finance_service"]["utxo_request_level"]
        # if configured load utxo
        if self.utxo_cache_enabled:
            self.load_utxo()

    def get_status(self) -> Dict[str, Any]:
        """ Return the status of the funding service
        """
        try:
            response = requests.get(self.service_url + "/status", timeout=self.timeout)
        except:
            raise FinancingServiceException("ConnectionError connecting to finance service. Check that the finance service is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise FinancingServiceException(f"ConnectionError connecting to finance service. Response = {response}.")
        return data

    def check_version(self):
        try:
            fs_status = self.get_status()
        except FinancingServiceException:
            pass
        else:
            # Check version
            try:
                assert fs_status is not None
                version = fs_status["version"]
            except KeyError:
                raise FinancingServiceException("Financing Service did not provide version")
            else:
                if Version(version) < Version(self.required_version):
                    raise FinancingServiceException(f"Financing Service needs to be version '{self.required_version}' or above.")

    def get_balance(self, client_id: str) -> Dict[str, Any]:
        """ Return the balance for provided client_id
        """
        try:
            response = requests.get(self.service_url + f"/client/{client_id}/balance", timeout=self.timeout)
        except:
            raise FinancingServiceException("ConnectionError connecting to finance service. Check that the finance service is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise FinancingServiceException(f"ConnectionError connecting to finance service. Response = {response}.")
        return data

    def get_address(self, client_id: str) -> Dict[str, Any]:
        """ Return the address for provided client_id
        """
        try:
            response = requests.get(self.service_url + f"/client/{client_id}/address", timeout=self.timeout)
        except:
            raise FinancingServiceException("ConnectionError connecting to finance service. Check that the finance service is running.")
        else:
            if response.status_code == 200:
                data = response.json()
                LOGGER.debug(f"data = {data}")
            else:
                LOGGER.debug(f"response = {response}")
                raise FinancingServiceException(f"ConnectionError connecting to finance service. Response = {response}.")
        return data

    def get_funds(self, id: str, fee_estimate: int, locking_script: str) -> Optional[Dict[str, Any]]:
        """ Get the funds for one tx
        """
        if self.utxo_cache_enabled:
            # if below the threshold get more tx in the cache
            if locking_script in self.utxo:
                if len(self.utxo[locking_script]) < self.utxo_min_level:
                    result = self._get_funds(id, fee_estimate, locking_script, self.utxo_request_level, False)
                    if result is None:
                        return None
                    else:
                        # add them to the cache
                        assert result["status"] == "Success"
                        self.utxo[locking_script].extend(result["outpoints"])
            else:
                result = self._get_funds(id, fee_estimate, locking_script, self.utxo_request_level, False)
                if result is None:
                    return None
                else:
                    # add them to the cache
                    assert result["status"] == "Success"
                    if locking_script not in self.utxo:
                        self.utxo[locking_script] = []
                    self.utxo[locking_script].extend(result["outpoints"])
            # Pop outpoint off the cache
            utxo = self.utxo[locking_script].pop()
            # Save utxo
            self.save_utxo()
            return {"status": "Success", "outpoints": [utxo]}
        else:
            return self._get_funds(id, fee_estimate, locking_script, 1, False)

    def _get_funds(self, id: str, fee_estimate: int, locking_script: str, no_of_outpoints: int, multiple_tx: bool) -> Optional[Dict[str, Any]]:
        """ Underlying get_funds call
        """
        fund_request = {
            "client_id": id,
            "satoshi": fee_estimate,
            "no_of_outpoints": no_of_outpoints,
            "multiple_tx": multiple_tx,
            "locking_script": locking_script,
        }
        response = requests.post(self.service_url + "/fund", timeout=self.timeout, json=fund_request)
        if response.status_code == 200:
            try:
                data = response.json()
            except json.decoder.JSONDecodeError as e:
                LOGGER.info(f"response = {response}")
                LOGGER.warning(f"error = {e}")
                return None
            else:
                LOGGER.debug(f"data = {data}")
                return data
        else:
            LOGGER.info(f"response = {response}")
            print(f"response.text = {response.text}")
            return None

    def load_utxo(self):
        if self.utxo_persistence_enabled:
            try:
                with open(self.utxo_file, 'r') as f:
                    self.utxo = json.load(f)
            except FileNotFoundError:
                pass

    def save_utxo(self):
        if self.utxo_persistence_enabled:
            # Convert to something we can write out
            with open(self.utxo_file, 'w') as f:
                json.dump(self.utxo, f)

    def cache_enabled(self) -> bool:
        return self.utxo_cache_enabled

    def cache_size(self) -> int:
        sz = 0
        if self.utxo_cache_enabled:
            for v in self.utxo.values():
                sz += len(v)
        return sz

    def add_info(self, client_id: str, wif: str) -> bool:
        url = self.service_url + f"/client"
        info_data = {
            "client_id": client_id,
            "wif": wif,
        }
        response = requests.post(url, timeout=self.timeout, json=info_data)
        data = None
        if response.status_code == 200:
            data = response.json()
            LOGGER.debug(f"data = {data}")
            return True
        else:
            LOGGER.debug(f"response = {response}")
            print(f"response.status_code = {response.status_code}")
            print(f"response.text = {response.text}")
            return False

    def delete_info(self, client_id: str) -> bool:
        url = self.service_url + f"/client/{client_id}"
        response = requests.delete(url, timeout=self.timeout)
        data = None
        if response.status_code == 200:
            data = response.json()
            LOGGER.debug(f"data = {data}")
            return True
        else:
            LOGGER.debug(f"response = {response}")
            return False
