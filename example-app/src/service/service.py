from typing import Dict, Any
from datetime import datetime

from config import ConfigType
from tx_engine import Wallet, Tx, TxIn, TxOut, Script
from tx_engine.engine.op_codes import OP_0, OP_RETURN

from service.financing_service import FinancingService, FinancingServiceException
from service.uaas_service import UaaSService, UaaSServiceException
from service.dynamic_config import dynamic_config


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
        self.tx_cost_amount: int = 500
        self.fs_client_id: str | None = None

    def set_dynamic_config(self):
        try:
            wif = dynamic_config["wif_key"]
        except KeyError:
            pass
        else:
            self.wallet = Wallet(wif)
        try:
            client_id = dynamic_config["client_id"]
        except KeyError:
            pass
        else:
            self.fs_client_id = client_id

    def set_config(self, config: ConfigType):
        """ Given the configuration, configure this service"""
        self.blockchain_enabled = config["app"]["blockchain_enabled"]
        self.tx_cost_amount = config["app"]["tx_cost_amount"]

        if self.blockchain_enabled:
            self.set_dynamic_config()

            self.financing_service = FinancingService()
            self.financing_service.set_config(config)
            self.uaas = UaaSService()
            self.uaas.set_config(config)

    def check_service_versions(self):
        if self.blockchain_enabled:
            self.financing_service.check_version()
            self.uaas.check_version()

    def is_blockchain_enabled(self) -> bool:
        return self.blockchain_enabled

    def get_status(self) -> Dict[str, Any]:
        """ Return the status of the appliction, financing service and UaaS service.
        """
        status = {
            "application_status": {
                "status": "Success",
                "current_time": time_as_str(datetime.now()),
                "blockchain_enabled": self.blockchain_enabled,
            }
        }
        if self.blockchain_enabled:
            try:
                status["financing_service_status"] = self.financing_service.get_status()
            except FinancingServiceException as e:
                status["financing_service_status"] = {"error": str(e)}
            try:
                uaas_status = self.uaas.get_status()
                status["uaas_status"] = uaas_status
            except UaaSServiceException as e:
                status["uaas_status"] = {"error": str(e)}
        return status

    def is_financing_service_running(self) -> bool:
        """ Returns true if application manages to contact financing service
        """
        if not self.blockchain_enabled:
            return False
        try:
            self.financing_service.get_status()
        except FinancingServiceException:
            return False
        else:
            return True

    def add_financing_service_key(self, client_id: str) -> Dict[str, Any]:
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

        if not self.financing_service.add_info(client_id, wif):
            return {
                "status": "Failure",
                "message": "Unable to add client to Financing Service"
            }
        # Record client_id to dynamic config
        dynamic_config["client_id"] = client_id
        self.set_dynamic_config()
        # Financing service should record the WIF
        return {
            "status": "Success",
            "Address": address,
        }

    def delete_financing_service_key(self, client_id: str) -> Dict[str, Any]:
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

        if not self.financing_service.delete_info(financing_service_client_id):
            return {
                "status": "Failure",
                "message": "Unable to remove client from the Financing Service"
            }

        # Remove client_id from dynamic config
        del dynamic_config["client_id"]
        self.set_dynamic_config()
        return {"status": "Success"}

    def get_balance(self) -> Dict[str, Any]:
        """ Return the blance of the client_id from FS
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

    def get_address(self) -> Dict[str, Any]:
        """ Return the address of the client_id from FS
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
            return self.financing_service.get_address(financing_service_client_id)
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

    def _create_data_tx(self, data: str) -> None | Tx:
        """ Create a tx with the course_name and certificate_id embedded
        """
        assert self.wallet is not None
        assert self.fs_client_id is not None
        fee_estimate = self.tx_cost_amount

        locking_script = self.wallet.get_locking_script().raw_serialize().hex()
        result = self.financing_service.get_funds(self.fs_client_id, fee_estimate, locking_script)
        if result is None:
            print("Unable to create funds")
            return None
        if result['status'] != "Success":
            return None
        print(f"result = {result}")

        outpoints = result['outpoints'][0]
        # Create vin
        vins = [TxIn(prev_tx=bytes.fromhex(outpoints['hash']), prev_index=outpoints['index'])]

        # Create vout with data
        encoded_data: bytes = f"ExApp,{data}".encode("utf-8")
        cert_script = Script([OP_0, OP_RETURN, encoded_data])
        vouts = [
            TxOut(amount=0, script_pubkey=cert_script),
        ]
        tx = Tx(version=1, tx_ins=vins, tx_outs=vouts, locktime=0)
        # Sign tx
        # tx = self.wallet.sign_tx(0, fund_tx, tx)
        if not tx:
            raise ValueError("Failed to sign & verify signature input before transmission")
        return tx

    def create_tx(self, data: str) -> Dict[str, Any]:
        """ Called by rest_api
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

        if self.fs_client_id is None:
            return {
                "status": "Failure",
                "message": "Application does not have financing service client_id"
            }

        tx = self._create_data_tx(data)

        print(f"tx = {tx}")

        return {
            "status": "Success",
        }


service = Service()
