
import unittest
import os
import sys
sys.path.append("..")

from service.service import service
from service.dynamic_config import dynamic_config

from test_config import DYNAMIC_CONFIG_FILE, CONFIG


class AppKeyTests(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(DYNAMIC_CONFIG_FILE)
        except FileNotFoundError:
            pass

    def test_app_key(self):
        """ Check of adding/removing an application key
        """
        dynamic_config.set_config(CONFIG)   # Needs to be called before service.set_config
        service.set_config(CONFIG)

        # Should succeed
        result = service.add_application_key()
        self.assertEqual(result["status"], 'Success')

        # Check file created
        self.assertTrue(os.path.isfile(DYNAMIC_CONFIG_FILE))

        # Should fail as we already have a key
        result = service.add_application_key()
        self.assertEqual(result["status"], 'Failure')

        # Should succeed
        result = service.delete_application_key()
        self.assertEqual(result["status"], 'Success')

        # Check file empty
        self.assertEqual(os.path.getsize(DYNAMIC_CONFIG_FILE), 0)

        # Should fail as there is no key
        result = service.delete_application_key()
        self.assertEqual(result["status"], 'Failure')


if __name__ == "__main__":
    unittest.main()
