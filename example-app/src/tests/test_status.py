
import unittest
import sys
sys.path.append("..")

from service.service import service

from test_config import CONFIG


class StatusTests(unittest.TestCase):

    def test_status(self):
        """ Check of status call
        """
        service.set_config(CONFIG)
        result = service.get_status()
        self.assertEqual(result["application_status"]["status"], 'Success')
        self.assertEqual(result["application_status"]["blockchain_enabled"], True)
        """
        result = {
            'application_status': {
                'status': 'Success',
                'current_time': '2024-11-15 11:42:26',
                'blockchain_enabled': True
            },
            'financing_service_status': {
                'version': '1.5.0',
                'blockchain_status': 'Connected',
                'blockchain_update_time': '2024-11-15 11:42:25'
            },
            'uaas_status': {
                'network': 'testnet',
                'version': 'unknown',
                'last block time': '2024-11-15 11:00:37',
                'block height': 1647058,
                'number of txs': 187338,
                'number of utxo entries': 182299,
                'number of mempool entries': 11
            }
        }
        """

    def test_is_finance_service_running(self):
        """ Check of FS status
        """
        service.set_config(CONFIG)
        result = service.is_financing_service_running()
        assert isinstance(result, bool)


if __name__ == "__main__":
    unittest.main()
