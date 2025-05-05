import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    __instance = None

    ALLOWED_STORAGE_TYPES = ["memory", "json", "sqlite"]

    def __new__(cls, *args, **kwargs):
        if cls.__instance  == None:
            cls.__instance = super().__new__(cls)
            cls.__instance.load()
        return cls.__instance
    
    def load(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "memory")
        self.db_name = os.getenv("DB_NAME", "tasks.db")
        self.json_file = os.getenv("JSON_FILE", "tasks.json")

    def validate(self):
        if self.storage_type not in self.ALLOWED_STORAGE_TYPES:
            raise ValueError(f"Invalid storage type: {self.storage_type}. Allowed types are: {', '.join(self.ALLOWED_STORAGE_TYPES)}")
        
            