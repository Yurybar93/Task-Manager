from storage.base import BaseStorage
from storage.memory import MemoryStorage
from storage.jsonfile import JSONFileStorage
from storage.sqlite import SQLiteStorage
from core.config import Config

class StorageFactory:
    _instances = {}

    @staticmethod
    def create_storage(storage_type: str, **kwargs) -> BaseStorage:
        """
        Factory method to create a storage instance based on the specified type.

        Parameters:
        ----------
        storage_type : str
            The type of storage to create (memory, jsonfile, sqlite).
        **kwargs : dict
            Additional parameters for specific storage types.
            - For jsonfile: filename (str) - Path to the JSON file. 
            - For sqlite: db_name (str) - Name of the SQLite database file.
        
        Returns:
        --------
            BaseStorage: An instance of the specified storage type. 

        Raises:
        -------
            ValueError: If the storage type is not recognized.
        """
        config = Config()

        cache_key  = storage_type or config.storage_type

        if cache_key in StorageFactory._instances:
            return StorageFactory._instances[cache_key]

        # if storage_type == 'memory':
        #     return MemoryStorage()
        # elif storage_type == 'jsonfile':
        #     filename = kwargs.get('filename', config.json_file)
        #     return JSONFileStorage(filename)
        # elif storage_type == 'sqlite':
        #     db_name = kwargs.get('db_name', config.db_name)
        #     return SQLiteStorage(db_name)
        # else:
        #     raise ValueError(f"Unknown storage type: {storage_type}")
         # Создаем и сохраняем
        if cache_key == 'memory':
            StorageFactory._instances[cache_key] = MemoryStorage()
        elif cache_key == 'jsonfile':
            filename = kwargs.get('filename', config.json_file)
            StorageFactory._instances[cache_key] = JSONFileStorage(filename)
        elif cache_key == 'sqlite':
            db_name = kwargs.get('db_name', config.db_name)
            StorageFactory._instances[cache_key] = SQLiteStorage(db_name)
        else:
            raise ValueError(f"Unknown storage type: {cache_key}")

        return StorageFactory._instances[cache_key]