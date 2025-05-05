import logging
from functools import wraps

class Logger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            
            cls.__instance.logger = logging.getLogger("TaskManager")
            cls.__instance.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler("task_manager.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            cls.__instance.logger.addHandler(file_handler)

        return cls.__instance
    
    def get_logger(self):
        return self.logger
    
    @staticmethod
    def log_action(func):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger = Logger().get_logger()
                logger.info(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"Completed {func.__name__}")
                return result
            return wrapper
        return decorator
  