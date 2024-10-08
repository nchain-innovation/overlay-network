from typing import Dict, Any
from datetime import datetime

from packaging.version import Version
from config import ConfigType
from tx_engine import Wallet
from service.financing_service import FinancingService, FinancingServiceException
from service.uaas_service import UaaSService, UaaSServiceException
from service.dynamic_config import dynamic_config

REQUIRED_FS_VERSION = "0.3.0"

class ApplicationException(Exception):
    pass


def time_as_str(time) -> str:
    if time is None:
        return "None"
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")


def read_config(config_field: Any) -> None | Any:
    try:
        value = config_field
    except KeyError:
        return None
    else:
        return value


class Service:
    """ This class represents the Orchestrator functionality in the design
    """
    def __init__(self):
        self.wallet: Wallet | None = None
        self.blockchain_enabled: bool = False

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.blockchain_enabled = config["app"]["blockchain_enabled"]
        if self.blockchain_enabled:
            try:
                wif = dynamic_config["wif_key"]
            except KeyError:
                pass
            else:
                self.wallet = Wallet(wif)

            self.financing_service = FinancingService()
            self.financing_service.set_config(config)
            self.uaas = UaaSService()
            self.uaas.set_config(config)

    def check_service_versions(self):
        if not self.blockchain_enabled:
            return
        try:
            fs_status = self.financing_service.get_status()
        except FinancingServiceException as e:
            pass
        else:        
            # check_version
            try:    
                version = fs_status["version"]
            except KeyError:
                raise ApplicationException("Financing Service did not provide version")
            else:
                if Version(version) < Version(REQUIRED_FS_VERSION):
                    raise ApplicationException(f"Financing Service needs to be '{REQUIRED_FS_VERSION}' or above.")


    def is_blockchain_enabled(self) -> bool:
        return self.blockchain_enabled

    def get_status(self) -> Dict[str, Any]:
        """ Return the service status
        """
        status = {
            "status": "Success",
            "current_time": time_as_str(datetime.now()),
            "blockchain_enabled": self.blockchain_enabled,
        }
        if self.blockchain_enabled:
            try:
                status["financing_service_status"] = self.financing_service.get_status()
            except FinancingServiceException as e:
                status["financing_service_status"] = str(e)
            try:
                status["uaas_status"] = self.uaas.get_status()
            except UaaSServiceException as e:
                status["uaas_status"] = str(e)
        return status

    def add_financing_service_info(self, client_id: str) -> Dict[str, Any]:
        """ Add key to the financing service to fund the transactions.
        """
        if not self.blockchain_enabled:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }
        if "client_id" in dynamic_config:
            # if self.financing_service_client_id is not None:
            return {
                "status": "Failure",
                "message": "Application has already has a client_id for the financing service"
            }
        tmp_wallet = Wallet.generate_keypair("BSV_Testnet")

        # Record WIF to dynamic config
        wif = tmp_wallet.to_wif()
        address = tmp_wallet.get_address()

        result = self.financing_service.add_info(client_id, wif)
        if result:
            pass
            # Record client_if and WIF to dynamic config
            dynamic_config["client_id"] = client_id
            # Financing service should record the WIF

        return {
            "status": "Success",
            "Address": address,
        }

    def delete_financing_service_info(self, client_id: str) -> Dict[str, Any]:
        """ Remove financing_service info
        """
        if not self.blockchain_enabled:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }
        try:
            financing_service_client_id = dynamic_config["client_id"]
        except KeyError:
            # if self.financing_service_client_id is None:
            return {
                "status": "Failure",
                "message": "Application has no client_id for the financing service"
            }

        result = self.financing_service.delete_info(financing_service_client_id)
        if result:
            # Remove client_id from dynamic config
            del dynamic_config["client_id"]
        return {
            "status": "Success",
        }

    def get_balance(self) -> Dict[str, Any]:
        """ Return the service status
        """
        if not self.blockchain_enabled:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }
        try:
            financing_service_client_id = dynamic_config["client_id"]
        except KeyError:
            # if self.financing_service_client_id is None:
            return {
                "status": "Failure",
                "message": "Application has no client_id for the financing service"
            }
        try:
            return self.financing_service.get_balance(financing_service_client_id)
        except FinancingServiceException as e:
            return {
                "status": "Failure",
                "message": str(e),
            }

    # Applicaton key
    def add_application_key(self) -> Dict[str, Any]:
        """ Add key to the application for creating transactions.
        """
        if not self.blockchain_enabled:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }

        if self.wallet is not None:
            return {
                "status": "Failure",
                "message": "Application already has a key"
            }

        self.wallet = Wallet.generate_keypair("BSV_Testnet")
        # Record WIF to dynamic config
        wif = self.wallet.to_wif()
        dynamic_config["wif_key"] = wif
        return {
            "status": "Success",
        }

    def delete_application_key(self) -> Dict[str, Any]:
        """ Remove application key
        """
        if not self.blockchain_enabled:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }

        if self.wallet is None:
            return {
                "status": "Failure",
                "message": "Application does not have a key"
            }

        del self.wallet
        self.wallet = None
        # Remove WIF from dynamic config
        del dynamic_config["wif_key"]
        return {
            "status": "Success",
        }


service = Service()
