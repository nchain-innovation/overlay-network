
import sys
sys.path.append("..")

from tx_engine import Wallet


if __name__ == '__main__':
    wallet = Wallet.generate_keypair("BSV_Testnet")
    print(f"wif = {wallet.to_wif()}")
    print(f"address = {wallet.get_address()}")
