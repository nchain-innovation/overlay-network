# Project


# Done

FS - no longer returns the names of clients in status message.
App - provide an endpoint for generating new keys
App - get balance from financing service
App - date format consitent in status message
FS - to query WoC even if there are no Clients, to check connectivity
FS - Change balance endpoint

    * EA - Get status/versions of services (FS & UaaS)
* EA - Add/Delete application key
* EA - Add unit tests


# In progress 
Remove client_id from financing_service.py

# To Do
* Build out Example Application
* EA - Timeouts on all request calls 
* EA - return correct error codes on responses


* Financing Service (FS)
    * Get FS to use UaaS
    * Move to main chain-gang, currently using a specific commit

* UTXO as a Service (UaaS)
    * Get UaaS to provide additional interface
    * See if can use leveldb to speed up UaaS updates
    * Provide version number

# Nice to have
* Prometheus/Grafana for System Monitoring?
    * Do we get this free with K8s?

# Questions


