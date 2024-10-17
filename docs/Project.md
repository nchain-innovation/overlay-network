# Project


# Done
FS - no longer returns the names of clients in status message.
FS - to query WoC even if there are no Clients, to check connectivity
FS - Change balance endpoint
FS - Move to main chain-gang, currently using a specific commit

App - provide an endpoint for generating new keys
App - get balance from financing service
App - date format consistent in status message
ES - Remove client_id from financing_service.py


* EA - Add/Delete application key
* EA - Add unit tests
* EA - Timeouts on all request calls 


# In progress 

* Build out Example Application

# To Do


* EA - return correct error codes on responses

* EA - Get status/versions of services (FS & UaaS)
    * waiting for UaaS version 

* Financing Service (FS)
    * Get FS to use UaaS
    * FS - to remove secp256k1


* UTXO as a Service (UaaS)
    * Provide version number
    * Get UaaS to provide additional interface
    * See if can use leveldb to speed up Tx updates
    * Need to ensure searching tx finds those in collections
    * refactor collections in database    
    * support for other miners, if main miner goes off line
    * provide the hash of the blockheader (to match WoC)


# Nice to have
* Prometheus/Grafana for System Monitoring?
    * Do we get this free with K8s?

* FS - add actions
* EA - add actions
* UaaS - add actions

# Questions


