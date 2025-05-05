import unittest
from unittest.mock import patch
from factory.storage_factory import StorageFactory
from storage.memory import MemoryStorage
from storage.jsonfile import JSONFileStorage
from storage.sqlite import SQLiteStorage
from core.config import Config

class TestStorageFactory(unittest.TestCase):
    def setUp(self):
        self.config_patch = patch('core.config.Config')
        self.mock_config = self.config_patch.start()
        self.mock_config.return_value.storage_type = 'memory'
        self.mock_config.return_value.json_file = 'test.json'
        self.mock_config.return_value.db_name = 'test.db'

    def tearDown(self):
        self.config_patch.stop()

    def test_create_memory_storage(self):
        storage = StorageFactory.create_storage('memory')
        self.assertIsInstance(storage, MemoryStorage)

    def test_create_jsonfile_storage(self):
        storage = StorageFactory.create_storage('jsonfile', filename='test.json')
        self.assertIsInstance(storage, JSONFileStorage)
        self.assertEqual(storage.filename, 'test.json')

    def test_create_sqlite_storage(self):
        storage = StorageFactory.create_storage('sqlite', db_name='test.db')
        self.assertIsInstance(storage, SQLiteStorage)
        self.assertEqual(storage.db_name, 'test.db')

    @patch('factory.storage_factory.Config')
    def test_create_default_storage(self, mock_config_class):
        mock_config = mock_config_class.return_value
        mock_config.storage_type = 'memory'

        storage = StorageFactory.create_storage(None)
        self.assertIsInstance(storage, MemoryStorage)

    def test_invalid_storage_type(self):
        with self.assertRaises(ValueError) as context:
            StorageFactory.create_storage('invalid_type')
        self.assertEqual(str(context.exception), "Unknown storage type: invalid_type")

    if __name__ == '__main__':
        unittest.main()