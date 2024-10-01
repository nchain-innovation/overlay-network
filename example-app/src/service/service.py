from config import ConfigType
from tx_engine import Wallet


class Service:
    """ This class represents the Orchestrator functionality in the design
    """
    def __init__(self):
        self.wallet: Wallet
        self.blockchain_enabled: bool = False

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.blockchain_enabled = config["orchestrator"]["blockchain_enabled"]
        if self.blockchain_enabled:
            wif = config["wallet"]["wif_key"]
            self.wallet = Wallet(wif)


service = Service()
