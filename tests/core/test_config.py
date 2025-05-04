import unittest
from unittest.mock import patch
from core.config import Config#
import os

class TestConfig(unittest.TestCase):
    """Unit tests for the Config class."""
    def setUp(self):
        """Set up the test environment."""
        Config._Config__instance = None

    def test_singleton(self):
        """Test that the Config class is a singleton."""
        config1 = Config()
        config2 = Config()
        self.assertIs(config1, config2)

    def test_load_env_variables(self):
        """Test loading configuration from environment variables."""
        os.environ['STORAGE_TYPE'] = 'json'
        os.environ['DB_NAME'] = 'test.db'
        os.environ['JSON_FILE'] = 'test.json'
        
        config = Config()

        self.assertEqual(config.storage_type, 'json')
        self.assertEqual(config.db_name, 'test.db')
        self.assertEqual(config.json_file, 'test.json')

    def test_load_default_values(self):
        """Test loading default values when environment variables are not set."""
        os.environ.pop('STORAGE_TYPE', None)
        os.environ.pop('DB_NAME', None)
        os.environ.pop('JSON_FILE', None)

        
        config = Config()

        self.assertEqual(config.storage_type, 'memory')
        self.assertEqual(config.db_name, 'tasks.db')
        self.assertEqual(config.json_file, 'tasks.json')

    def test_invalid_storage_type(self):
        """Test that an invalid storage type raises a ValueError."""
        os.environ['STORAGE_TYPE'] = 'invalid_type'
        
        with self.assertRaises(ValueError) as context:
            config = Config()
            config.validate()

        self.assertEqual(str(context.exception), "Invalid storage type: invalid_type. Allowed types are: memory, json, sqlite")

    def tearDown(self):
        """Clean up the test environment."""
        os.environ.pop('STORAGE_TYPE', None)
        os.environ.pop('DB_NAME', None)
        os.environ.pop('JSON_FILE', None)
        Config._Config__instance = None

if __name__ == '__main__':
    unittest.main()