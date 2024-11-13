# Configuration

Configuration for this Application can be found in the `data\example-app.toml` TOML file.

The toml file is read when the Application starts.

The file is composed of the following sections:


## [web_interface]
This provides the settings for the Applications's Swagger interface.

``` TOML
[web_interface]
address = '0.0.0.0:3050'
log_level = 'debug'
reload = false
origins = ["*"]
```

## [app]

The Application's settings.
``` TOML
[app]
blockchain_enabled = true
tx_cost_amount = 500
```

## [wallet]
``` TOML
[wallet]
# wif_key = "cSH2NR16zKeEcWR6Cqvh61aouzbk8ShhWgZXVEWnnR1YNQrfQvkB"
# address = "mqzGJVq37wHn2zcnH9rMDzqGs5sFMqkgrc"
```


## [finance_service]
This provides detials for the `Application` to connect to the `Financing Service`.

``` TOML
[finance_service]
url = "http://host.docker.internal:8082"
# url = "http://127.0.0.1:8082"
# client_id = "id1"
utxo_cache_enabled = false
utxo_persistence_enabled = true
utxo_file = "../data/utxo.json"
utxo_min_level = 100
utxo_request_level = 500
```
## [uaas]
This provides detials for the `Application` to connect to the `UTXO as a Service` (UaaS).
``` TOML
[uaas]
url = "http://host.docker.internal:5010"
```

## [dynamic_config]
This provides details for the `Application` to obtain it's dynamic configuration.
The dynamic configuration stores:
* `client_id` - for the Financing Service
* `wif` - for the Application Key

``` TOML
[dynamic_config]
filename = "../data/dynamic.toml
```