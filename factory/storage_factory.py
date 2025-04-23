from storage.base import BaseStorage
from storage.memory import MemoryStorage
from storage.jsonfile import JSONFileStorage
from storage.sqlite import SQLiteStorage

class StorageFactory:
    @staticmethod
    def create_storage(storage_type: str, **kwargs) -> BaseStorage:
        if storage_type == 'memory':
            return MemoryStorage()
        elif storage_type == 'jsonfile':
            filename = kwargs.get('filename', 'tasks.json')
            return JSONFileStorage(filename)
        elif storage_type == 'sqlite':
            db_name = kwargs.get('db_name', 'tasks.db')
            return SQLiteStorage(db_name)
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")