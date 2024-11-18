
""" Configuration used by the tests
"""


DYNAMIC_CONFIG_FILE = "data/dynamic.toml"


CONFIG = {
    'app': {
        'blockchain_enabled': True,
        "tx_cost_amount": 500
    },
    'finance_service': {
        "required_version": "1.5.0",
        'url': 'http://host.docker.internal:8082',
        'utxo_cache_enabled': False,
        'utxo_persistence_enabled': True,
        'utxo_file': '../data/utxo.json',
        'utxo_min_level': 100,
        'utxo_request_level': 500
    },
    'uaas': {
        "required_version": "0.2.0",
        'url': 'http://host.docker.internal:5010'
    },
    'dynamic_config': {'filename': DYNAMIC_CONFIG_FILE}
}
