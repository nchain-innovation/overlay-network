
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
        self.assertEqual(result["status"], 'Success')
        self.assertEqual(result["blockchain_enabled"], True)
        """
        result = {
            'status': 'Success',
            'current_time': '2024-10-09 11:15:18',
            'blockchain_enabled': True,
            'financing_service_status': 'ConnectionError connecting to finance service. Check that the finance service is running.',
            'uaas_status': 'ConnectionError connecting to UaaS. Check that the UaaS is running.'
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
