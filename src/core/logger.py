import logging
import os
from functools import wraps

class Logger:
    """
    Singleton Logger class for logging actions in the application.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            base_dir = os.path.dirname(os.path.dirname(__file__))  
            log_dir = os.path.join(base_dir, "core", "config")
            os.makedirs(log_dir, exist_ok=True)

            log_path = os.path.join(log_dir, "task_manager.log")

            logger = logging.getLogger("TaskManager")
            logger.setLevel(logging.INFO)

            logger.handlers.clear()

           
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s'
                ))

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

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
