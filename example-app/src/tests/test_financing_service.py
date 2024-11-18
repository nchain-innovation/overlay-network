import unittest
import os
import sys
sys.path.append("..")

from service.service import service, Service
from service.dynamic_config import dynamic_config

from test_config import CONFIG, DYNAMIC_CONFIG_FILE


def check_financing_service() -> bool:
    s = Service()
    s.set_config(CONFIG)
    return s.is_financing_service_running()


financing_service_not_running = not check_financing_service()


class FinancingServiceTests(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(DYNAMIC_CONFIG_FILE)
        except FileNotFoundError:
            pass

    @unittest.skipIf(financing_service_not_running, "Financing Service is not running")
    def test_status(self):
        """ Check of status call
        """
        service.set_config(CONFIG)
        result = service.get_status()
        self.assertEqual(result["application_status"]["status"], 'Success')
        self.assertEqual(result["application_status"]["blockchain_enabled"], True)

        version = result["financing_service_status"]['version']
        self.assertTrue(isinstance(version, str))
        blockchain_status = result["financing_service_status"]['blockchain_status']
        self.assertTrue(blockchain_status in ['Connected', 'Unknown', 'Failed'])

        self.assertEqual(result['uaas_status']['network'], 'testnet')
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

    @unittest.skipIf(financing_service_not_running, "Financing Service is not running")
    def test_fs_clients(self):
        """ Check of client operations
        """
        dynamic_config.set_config(CONFIG)   # Needs to be called before service.set_config
        service.set_config(CONFIG)

        # Add client
        client_id = "wxyw"
        result = service.add_financing_service_key(client_id)
        self.assertEqual(result["status"], 'Success')
        """
        result = {
            'status': 'Success',
            'Address': 'n1RNk16BpoFmfqpg9hq1juqi5tSJgC3Dpg'
        }
        """
        # Check file created and has content
        self.assertTrue(os.path.isfile(DYNAMIC_CONFIG_FILE))
        self.assertGreater(os.path.getsize(DYNAMIC_CONFIG_FILE), 0)

        # Try again, should fail
        result = service.add_financing_service_key(client_id)
        self.assertEqual(result["status"], 'Failure')

        # Get balance of client
        result = service.get_balance()
        """
        result = {
            'confirmed': 0,
            'unconfirmed': 0
        }
        """
        self.assertIsNotNone(result["confirmed"])
        self.assertIsNotNone(result["unconfirmed"])

        # Remove client
        result = service.delete_financing_service_key(client_id)
        """
        result = {'status': 'Success'}
        """
        self.assertEqual(result["status"], 'Success')

        # check file is empty
        self.assertEqual(os.path.getsize(DYNAMIC_CONFIG_FILE), 0)

        # Remove client - should fail
        result = service.delete_financing_service_key(client_id)
        """
        result = .{'status': 'Failure', 'message': 'Application has no client_id for the financing service'}
        """
        self.assertEqual(result["status"], 'Failure')

    def test_fs_balance_failure(self):
        """ Check balance of unknown client
        """
        dynamic_config.set_config(CONFIG)   # Needs to be called before service.set_config
        service.set_config(CONFIG)

        # Get balance of client
        result = service.get_balance()
        """
        result = {
            'status': 'Failure',
            'message': 'Application has no client_id for the financing service'
        }
        """
        self.assertEqual(result["status"], 'Failure')


if __name__ == "__main__":
    unittest.main()
