import unittest
import os
from export.export import export_tasks
from models.task import Task, TaskStatus

class TestExportTasks(unittest.TestCase):
    """
    Test case for exporting tasks to different formats.
    """
    def setUp(self):
        """
        Set up the test case with sample tasks and a temporary file name.
        """
        self.tasks = [
            Task(title="Task 1", description="Description 1", status=TaskStatus.PENDING),
            Task(title="Task 2", description="Description 2", status=TaskStatus.COMPLETED),
        ]
        self.filename = "testfile"
        
    def test_export_valid_formats(self):
        """
        Test exporting tasks to valid formats (CSV, JSON, Markdown).
        """
        for format in ['csv', 'json', 'markdown']:
            output_file = export_tasks(self.tasks, f"{self.filename}.{format}", format)
            self.assertTrue(os.path.exists(output_file), f"File {output_file} was not created.")
            os.remove(output_file)

    def test_export_invalid_format(self):
        """
        Test exporting tasks to an invalid format.
        """
        with self.assertRaises(ValueError):
            export_tasks(self.tasks, f"{self.filename}.txt", "txt")

    
if __name__ == '__main__':
    unittest.main()