#!/usr/bin/python3

import uvicorn
import os

from fastapi.middleware.cors import CORSMiddleware

from config import load_config, ConfigType
from service.service import service

from rest_api import app

CONFIG_FILE = "../data/example-app.toml"


# Configure CORS for app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_webserver_config(app_name: str, config: ConfigType):
    address = config["address"]
    (host, port) = address.split(":")

    server_config = uvicorn.Config(
        app=app_name,
        host=host,
        port=int(port),
        log_level=config["log_level"],
        reload=config["reload"],
        workers=1)
    return server_config


def run_webserver(config: ConfigType):
    if os.environ.get("APP_TYPE") == "admin":
        server_config = create_webserver_config("admin_rest_api:admin_app", config['web_admin_interface'])
    else:
        server_config = create_webserver_config("rest_api:app", config['web_interface'])
    server = uvicorn.Server(server_config)
    server.run()


""" Setup and configure services
"""


def main():
    """ main function - reads config, sets up system, starts REST API
    """
    config = load_config(CONFIG_FILE)
    service.set_config(config)

    run_webserver(config)


if __name__ == "__main__":
    main()
