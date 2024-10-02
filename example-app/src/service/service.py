from typing import Dict, Any
from datetime import datetime

from config import ConfigType
from tx_engine import Wallet
from service.financing_service import FinancingService, FinancingServiceException


def time_as_str(time) -> str:
    if time is None:
        return "None"
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")


class Service:
    """ This class represents the Orchestrator functionality in the design
    """
    def __init__(self):
        self.wallet: Wallet
        self.blockchain_enabled: bool = False

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.blockchain_enabled = config["app"]["blockchain_enabled"]
        if self.blockchain_enabled:
            wif = config["wallet"]["wif_key"]
            self.wallet = Wallet(wif)
            self.financing_service = FinancingService()
            self.financing_service.set_config(config)

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

        return status

    def get_balance(self) -> Dict[str, Any]:
        """ Return the service status
        """
        if self.blockchain_enabled:
            try:
                return self.financing_service.get_balance()
            except FinancingServiceException as e:
                return {
                    "status": "Failure",
                    "message": str(e),
                }
        else:
            return {
                "status": "Failure",
                "message": "Blockchain is not enabled in the application"
            }


service = Service()
