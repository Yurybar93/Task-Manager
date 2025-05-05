import unittest
from unittest.mock import patch
from core.config import Config#
import os

class TestConfig(unittest.TestCase):
    def setUp(self):
        Config._Config__instance = None

    def test_singleton(self):
        config1 = Config()
        config2 = Config()
        self.assertIs(config1, config2)

    def test_load_env_variables(self):
        os.environ['STORAGE_TYPE'] = 'json'
        os.environ['DB_NAME'] = 'test.db'
        os.environ['JSON_FILE'] = 'test.json'
        
        config = Config()

        self.assertEqual(config.storage_type, 'json')
        self.assertEqual(config.db_name, 'test.db')
        self.assertEqual(config.json_file, 'test.json')

    def test_load_default_values(self):
        os.environ.pop('STORAGE_TYPE', None)
        os.environ.pop('DB_NAME', None)
        os.environ.pop('JSON_FILE', None)

        
        config = Config()

        self.assertEqual(config.storage_type, 'memory')
        self.assertEqual(config.db_name, 'tasks.db')
        self.assertEqual(config.json_file, 'tasks.json')

    def test_invalid_storage_type(self):
        os.environ['STORAGE_TYPE'] = 'invalid_type'
        
        with self.assertRaises(ValueError) as context:
            config = Config()
            config.validate()

        self.assertEqual(str(context.exception), "Invalid storage type: invalid_type. Allowed types are: memory, json, sqlite")

    def tearDown(self):
        os.environ.pop('STORAGE_TYPE', None)
        os.environ.pop('DB_NAME', None)
        os.environ.pop('JSON_FILE', None)
        Config._Config__instance = None

if __name__ == '__main__':
    unittest.main()