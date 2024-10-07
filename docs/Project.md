# Project


# Done

FS - no longer returns the names of clients in status message.
App - provide an endpoint for generating new keys
App - get balance from financing service
App - date format consitent in status message
FS - to query WoC even if there are no Clients, to check connectivity

    * EA - Get status/versions of services (FS & UaaS)


# In progress 
Remove client_id from financing_service.py

# To Do
* Build out Example Application
* EA - Timeouts on all request calls 



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


