import sys
sys.path.append("..")
import json

from tx_engine import interface_factory, Script, Tx, TxIn, TxOut

CONFIG = {
    "interface_type": "rpc",
    "network_type": "testnet",
    "user": "bitcoin",
    "password": "bitcoin",
    "address": "host.docker.internal:18332"
}

def main():
    interface = interface_factory.set_config(CONFIG)
    ret = interface._get_chain_info()
    print(ret)

    ret = interface.get_info()
    print(ret)
    print("-----")
    script = Script.parse_string('0x01 OP_2 OP_NUM2BIN 0x0100 OP_EQUAL')
    s = script.serialize().hex()
    # j = json.dumps([{"tx":s}])
    # j = json.dumps([{"tx": s}])
    # bitcoinrpc.authproxy.JSONRPCException: -1: JSON value is not an object as expected
    j = json.dumps([{"tx": s}])
    # bitcoinrpc.authproxy.JSONRPCException: -1: JSON value is not an object as expected

    print(f"j = {j}")
    # 080101528002010087
    #ret = interface.verifyscript(scripts=[j], stopOnFirstInvalid=True, totalTimeout=100)

    tx_hash: str = "01000000019d2e185c5cc6e8d01374a3d10b1872f88e3cfc0fdd7c1dd61ccc12d73ff8a494000000006b483045022100da199cb41d1798a736bfa8dfcfaf30a5f720a8637dbf6be42a979487445af6100220637a27a1342a79210c5576540127a14ad893b01daeaf9360125885de776e9116412103263ca7eebc4f31fefeff3d57e17091e4c672e9715241eb707dda7beb710e2384ffffffff0210270000000000001976a914b1434c4fcb4590be1ed7f4f9edce199243f36dea88acc4a19a3b000000001976a914da2f0c2c6786b2d46180551d57966cd89bbb03a788ac00000000"
    
    """
    txo_params = json.dumps([{
        "tx":tx_hash, 
        
        "script_pubkey" : "76a914da2f0c2c6786b2d46180551d57966cd89bbb03a788ac",
        "amount": 1000000000,
        "index": 0,
        "flags": (1 << 16),
    }])
    """

    txo_params = json.dumps({
        "tx":tx_hash, 
        "n": 0,
    })
    

    ret = interface.verifyscript([txo_params])

    print(ret)

"""
curl --data-binary '{"jsonrpc":"1.0","id":"curltext","method":"getblockchaininfo","params":[]}' -H 'content-type:text/plain;' http://bitcoin:bitcoin@127.0.0.1:18332/

{"result":{"chain":"regtest","blocks":9,"headers":9,"bestblockhash":"4d9a4443e6485a384896bdbd0f8e97f65a3ef27aaeab78e014e90f7475c613c2","difficulty":4.656542373906925e-10,"mediantime":1724422640,"verificationprogress":1,"chainwork":"0000000000000000000000000000000000000000000000000000000000000014","pruned":false,"softforks":[{"id":"bip34","version":2,"reject":{"status":false}},{"id":"bip66","version":3,"reject":{"status":false}},{"id":"bip65","version":4,"reject":{"status":false}},{"id":"csv","version":5,"reject":{"status":false}}]},"error":null,"id":"curltext"}


curl --data-binary '{"jsonrpc":"1.0","id":"curltext","method":"verifyscript","params":[[{"tx":"080101528002010087"}]]}' -H 'content-type:text/plain;' http://bitcoin:bitcoin@127.0.0.1:18332/


"""


if __name__ == '__main__':
    main()
