import logging
from functools import wraps

class Logger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            
            logger = logging.getLogger("TaskManager")
            logger.setLevel(logging.INFO)

            if not logger.handlers:
                file_handler = logging.FileHandler("task_manager.log")
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

            cls.__instance.logger = logger

        return cls.__instance
    
    def get_logger(self):
        return self.logger
    
    @staticmethod
    def log_action(description=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger = Logger().get_logger()
                name = description or func.__name__
                logger.info(f"→ Executing: {name} | args={args}, kwargs={kwargs}")
                try:
                    result = func(*args, **kwargs)
                    logger.info(f"✓ Completed: {name}")
                    return result
                except Exception as e:
                    logger.exception(f"✗ Error in: {name} — {e}")
                    raise
            return wrapper
        return decorator
        
  