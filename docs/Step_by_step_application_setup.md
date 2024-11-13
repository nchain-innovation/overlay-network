# Step by step Application setup


This document details how to setup the Application step by step.

The steps are 

1. Build the Docker Image
2. Run the Docker Image
3. Check System Status
4. Create Financing Service Key
5. Fund Financing Service Key
6. Check the Financing Service Address Balance



# 1) Build the Docker Image
``` bash
% cd example-app
% ./build.sh
```

# 2) Run the Docker Image
```bash
% cd example-app
% ./run.sh
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3050 (Press CTRL+C to quit)
```

This will start a Swagger web server at http://127.0.0.1:3050/docs (depending on configuration) which should look like this:

![Swagger](../docs/diagrams/example-app.png)


# 3) Check the System Status

1. Expand the `Status` section of the Swagger interface.
2. Click on the "Try it out" button 
3. Click on the "Execute" button 

You should see a response similar to:
![Status Response](../docs/diagrams/status_response.png)


Here we are looking for 
* `"blockchain_enabled": true` - from the Application Status section.
* `"blockchain_status": Connected` - from the Financing Service Status section.
* `"last block time":` - from the UaaS Status, within 30 minutes of the `current_time` provided by the Application status, this means that the UaaS is current with the blockchain.


If there are any issues with any of the above then either the supporting services are not running or the Application configuration is incorrect.
The configuration of the Example Application can be found in the TOML file `/data/example-app.toml`. 

The TOML configuration file also provides information about how to connect to the `Financing Service` and `UTXO as a Service`.

More details can be found [here](../docs/Configuration.md)



# 4) Create Financing Service Key

This section detials the process of generating the Financing Service Key. 

This key will be used by the Financing service to fund the Applications transactions.

![Create Financing Service Key](diagrams/create_fs_key_sequence.png)


Click on the Application Swagger interface, then:
1. Expand the `Add Financing Service Info` section of the Swagger interface.
2. Click on the "Try it out" button.
3. Enter a `client_id` into the text box.
4. Click on the "Execute" button.

< Show response here>

This shows the Address associated with the Financing Service Key. 

Keep a note of this address as we will need it in the next step.

# 5). Fund Financing Service Key

Once the Financing Service Key has been generated it needs to be funded.

Funds are provided by a testnet Facuet, such as https://witnessonchain.com/faucet/tbsv

This needs to be provided with the Financing Service Key's Address, that we obtained from the previous step.

On the Facuet website:
1. Enter the Financing Service Key's Address into the text box.
2. Click on the "Verify you are human" check box.
3. Click on the "Shoot me the coin" button.

The Facuet should provide some indication that the sending of funds was successful.

It can take a few minutes for the funds to arrive.

# 6). Check the Financing Service Address Balance
Click on the Application Swagger interface, then:
1. Expand the `Get Balance` section of the Swagger interface.
2. Click on the "Try it out" button.
3. Click on the "Execute" button.

The response should look like:

![Balance Response](diagrams/balance_response.png)

This indicates that there are confirmed and/or unconfirmed satoshis associated with this address.



