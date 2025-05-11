import os
from dotenv import load_dotenv
load_dotenv()

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "config", ".env")
load_dotenv(env_path)

class Config:
    """
    Singleton class to manage configuration settings for the application.

    Attributes:
    ------------
    storage_type (str): Type of storage to use (memory, json, sqlite).
    db_name (str): Name of the SQLite database file.
    json_file (str): Path to the JSON file for storing tasks.
    
    """
    __instance = None

    ALLOWED_STORAGE_TYPES = ["memory", "json", "sqlite"]

    def __new__(cls, *args, **kwargs):
        if cls.__instance  == None:
            cls.__instance = super().__new__(cls)
            cls.__instance.load()
        return cls.__instance
    
    def load(self):
        """
        Load configuration settings from environment variables or set default values.
        """
        self.storage_type = os.getenv("STORAGE_TYPE", "memory")
        self.db_name = os.getenv("DB_NAME", "tasks.db")
        self.json_file = os.getenv("JSON_FILE", "tasks.json")

    def validate(self):
        """
        Validate the configuration settings.
        Raises:
        --------
        ValueError: If the storage type is not allowed.
        """
        if self.storage_type not in self.ALLOWED_STORAGE_TYPES:
            raise ValueError(f"Invalid storage type: {self.storage_type}. Allowed types are: {', '.join(self.ALLOWED_STORAGE_TYPES)}")
        
            