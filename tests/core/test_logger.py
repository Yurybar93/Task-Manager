import unittest
from unittest.mock import patch
from core.logger import Logger
import logging
from io import StringIO

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_output = StringIO()
        self.logger = Logger().get_logger()
        self.logger.handlers = [] 

        stream_handler = logging.StreamHandler(self.log_output)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)

    def test_singleton(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertIs(logger1, logger2)

    def test_log_action_decorator(self):
        @Logger.log_action()
        def sample_function(x, y):
            return x + y

        result = sample_function(1, 2)
        self.assertEqual(result, 3)

        log_contents = self.log_output.getvalue()
        self.assertIn("sample_function", log_contents)
        self.assertIn("args=(1, 2)", log_contents)

    def test_log_action_decorator_exception(self):
        @Logger.log_action("failing function")
        def sample_function(x, y):
            raise ValueError("An error occurred")

        with self.assertRaises(ValueError):
            sample_function(1, 2)

        log_contents = self.log_output.getvalue()
        self.assertIn("→ Executing: failing function", log_contents)
        self.assertIn("args=(1, 2)", log_contents)
        self.assertIn("✗ Error in: failing function — An error occurred", log_contents)

if __name__ == '__main__':
    unittest.main()