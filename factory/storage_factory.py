from storage.base import BaseStorage
from storage.memory import MemoryStorage
from storage.jsonfile import JSONFileStorage
from storage.sqlite import SQLiteStorage
from core.config import Config

class StorageFactory:
    @staticmethod
    def create_storage(storage_type: str, **kwargs) -> BaseStorage:
        config = Config()

        storage_type = storage_type or config.storage_type

        if storage_type == 'memory':
            return MemoryStorage()
        elif storage_type == 'jsonfile':
            filename = kwargs.get('filename', config.json_file)
            return JSONFileStorage(filename)
        elif storage_type == 'sqlite':
            db_name = kwargs.get('db_name', config.db_name)
            return SQLiteStorage(db_name)
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")