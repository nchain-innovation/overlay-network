
from fastapi import FastAPI
from typing import Dict, Any

from tx_engine import Wallet

from service.service import service


tags_metadata = [
    {
        "name": "Example Application REST API",
        "description": "Example Application REST API",
    },
]


app = FastAPI(
    title="Example Application REST API",
    description="Example Application REST API",
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["Web"])
def root() -> Dict[str, str]:
    """ Web server Root
    """
    return {
        "name": "Example Application REST API",
        "description": "Example Application REST API",
    }


# Service Status
@app.get("/status", tags=["Status"])
def get_status() -> Dict[str, Any]:
    """ Return the current service status """
    return service.get_status()


# Endpoint to generate keys
@app.get("/generate_keys", tags=["Admin"])
def get_generate_keys() -> Dict[str, Any]:
    """ Generate a keypair for use by the application.
        Returns the WIF (Wallet Independent Format) private key and the
        associated public address.
    """
    wallet = Wallet.generate_keypair("BSV_Testnet")
    return {
        "wif": wallet.to_wif(),
        "address": wallet.get_address(),
    }


@app.get("/balance", tags=["Admin"])
def get_balance() -> Dict[str, Any]:
    """ Get balance from Financing service """
    return service.get_balance()
