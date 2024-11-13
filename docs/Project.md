# Project


# Done
* Financing Service
    * no longer returns the names of clients in status message.
    * to query WoC even if there are no Clients, to check connectivity
    * Change balance endpoint
    * Move to main chain-gang, currently using a specific commit

* Example App 
    * provide an endpoint for generating new keys
    * get balance from financing service
    * date format consistent in status message
    * Remove client_id from financing_service.py
    * Add/Delete application key
    * Add unit tests

    * Timeouts on all request calls 
    * Get status/versions of services (FS & UaaS)
        * (waiting for UaaS version)


* UaaS
    * Provide version number
    * Need to ensure searching tx finds those in collections
    * refactor collections in database    


# In progress 

* Build out Example Application

# To Do

* EA - return correct error codes on responses

* Financing Service (FS)
    * Get FS to use UaaS
    * FS - to remove secp256k1


* Chain Gang
    * Add UaaS Interface
    * Add UaaS interface tests to project

* UTXO as a Service (UaaS)
    * Get UaaS to provide additional interface
    * See if can use leveldb to speed up Tx updates
    * Utxo as level db 
    * support for other miners, if main miner goes off line
    * provide the hash of the blockheader (to match WoC)


# Nice to have
* Prometheus/Grafana for System Monitoring?
    * Do we get this free with K8s?

* FS - add actions
* EA - add actions
* UaaS - add actions

# Questions


