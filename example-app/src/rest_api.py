
from fastapi import FastAPI
from typing import Dict, Any

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


# Endpoint to add add_financing_service_info
@app.post("/financing_service_info", tags=["Financing Service Admin"])
def add_financing_service_info(client_id: str) -> Dict[str, Any]:
    """ Add info to the financing_service.
    """
    return service.add_financing_service_info(client_id)


@app.delete("/financing_service_info", tags=["Financing Service Admin"])
def delete_financing_service_info(client_id: str) -> Dict[str, Any]:
    """ Remove financing_service info
    """
    return service.delete_financing_service_info(client_id)


@app.get("/balance", tags=["Financing Service Admin"])
def get_balance() -> Dict[str, Any]:
    """ Get balance from Financing service """
    return service.get_balance()


@app.post("/application_key", tags=["Application Admin"])
def add_application_key() -> Dict[str, Any]:
    """ Add generate an application key and store it
    """
    return service.add_application_key()


@app.delete("/application_key", tags=["Application Admin"])
def delete_application_key() -> Dict[str, Any]:
    """ Remove application key
    """
    return service.delete_application_key()
