import unittest
import iterative_metrics

class TestConfig(unittest.TestCase):
    def test_config_loading(self):
        config = iterative_metrics.config.config("./tests/config.yml")
        password = config.get_component("database").get("password")
        self.assertEqual(password,"newpassword")


if __name__ =='__main__':
    unittest.main()