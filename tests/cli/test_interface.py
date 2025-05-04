import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import ANY
from cli.interface import handle_add_task, handle_get_task, handle_delete_task, handle_list_tasks, handle_update_task, handle_export_tasks
from models.task import Task, TaskStatus
from datetime import datetime, timedelta

class TestCLIInterface(unittest.TestCase):
    """
    Test cases for the CLI interface functions.
    These tests cover the functionality of adding, retrieving,
    deleting, listing, updating, and exporting tasks.
    """
    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.Task')
    def test_handle_add_task(self, mosk_task_cls, mock_create_storage):
        """
        Test adding a task using the CLI interface.
        This test checks if the task is created with the correct parameters
        and if the storage's add_task method is called.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        mock_task_instance = MagicMock()
        mosk_task_cls.return_value = mock_task_instance

        args = MagicMock()
        args.title = "Test Task"
        args.description = "This is a test task."
        args.deadline = "2023-10-01 12:00:00"
        args.storage_type = "memory"

        handle_add_task(args)

        mosk_task_cls.assert_called_once_with(
            title="Test Task",
            description="This is a test task.",
            deadline=ANY
        )
    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    def test_handle_get_task_found(self, mock_print, mock_create_storage):
        """
        Test retrieving a task by ID using the CLI interface.
        This test checks if the correct task is retrieved and if the storage's get_task method is called.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        mock_task = MagicMock()
        mock_storage.get_task.return_value = mock_task

        args = MagicMock()
        args.task_id = 1
        args.storage_type = "memory"

        handle_get_task(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.get_task.assert_called_once_with(1)
        mock_print.assert_called_once_with(f"Task found: {mock_task}")

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    def test_handle_get_task_not_found(self, mock_print, mock_create_storage):
        """
        Test retrieving a task by ID when the task is not found.
        This test checks if the correct message is printed when the task is not found.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        mock_storage.get_task.return_value = None

        args = MagicMock()
        args.task_id = 1
        args.storage_type = "memory"

        handle_get_task(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.get_task.assert_called_once_with(1)
        mock_print.assert_called_once_with(f"Task with ID {args.task_id} not found.")

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    def test_handle_delete_task(self, mock_print, mock_create_storage):
        """
        Test deleting a task by ID using the CLI interface.
        This test checks if the task is deleted and if the storage's delete_task method is called.
        """
        mock_storage = MagicMock()
        mock_storage.delete_task.return_value = True
        mock_create_storage.return_value = mock_storage

        args = MagicMock()
        args.task_id = 1
        args.storage_type = "memory"

        handle_delete_task(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.delete_task.assert_called_once_with(1)
        mock_print.assert_called_once_with(f"Task with ID {args.task_id} deleted.")

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.TaskIterator')
    @patch('cli.interface.print')
    def test_handle_list_tasks_without_filter(self, mock_print, mock_task_iterator_cls, mock_create_storage):
        """
        Test listing tasks without any filters using the CLI interface.
        This test checks if all tasks are listed and if the storage's list_tasks method is called.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_storage.list_tasks.return_value = [mock_task1, mock_task2]

        mock_task_iterator = MagicMock()
        mock_task_iterator.__iter__.return_value = iter([mock_task1, mock_task2])
        mock_task_iterator_cls.return_value = mock_task_iterator

        args = MagicMock()
        args.storage_type = "memory"
        args.status = None
        args.deadline = None

        handle_list_tasks(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.list_tasks.assert_called_once_with()
        mock_task_iterator_cls.assert_called_once_with([mock_task1, mock_task2])
        mock_print.assert_any_call(mock_task1)
        mock_print.assert_any_call(mock_task2)
        self.assertNotIn(
            unittest.mock.call("No tasks found."), 
                         mock_print.call_args_list
        )

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.TaskIterator')
    @patch('cli.interface.print')
    def test_handle_list_tasks_invalid_deadline(self, mock_print, mock_task_iterator_cls, mock_create_storage):
        """
        Test listing tasks with an invalid deadline format.
        This test checks if the correct error message is printed when the deadline format is invalid.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage
        mock_storage.list_tasks.return_value = []

        mock_iterator_instance = MagicMock()
        mock_task_iterator_cls.return_value = mock_iterator_instance

        args = MagicMock()
        args.storage_type = "memory"
        args.status = None
        args.deadline = "invalid_date"

        handle_list_tasks(args)

        mock_print.assert_called_once_with("Invalid date format. Use YYYY-MM-DD HH:MM:SS")
        mock_create_storage.assert_called_once_with("memory")
        mock_storage.list_tasks.assert_called_once()

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    def test_handle_update_task_success(self, mock_print, mock_create_storage):
        """
        Test updating a task by ID using the CLI interface.
        This test checks if the task is updated and if the storage's update_task method is called.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        mock_task = MagicMock()
        mock_storage.get_task.return_value = mock_task

        args = MagicMock()
        args.task_id = 1
        args.title = "Updated Task"
        args.status = "COMPLETED"
        args.description = "Updated description."
        args.deadline = "2023-10-01 12:00:00"
        args.storage_type = "memory"

        handle_update_task(args)

        self.assertEqual(mock_task.title, "Updated Task")
        self.assertEqual(mock_task.description, "Updated description.")
        self.assertEqual(mock_task.deadline, datetime.strptime("2023-10-01 12:00:00", '%Y-%m-%d %H:%M:%S'))

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.get_task.assert_called_once_with(1)
        mock_print.assert_called_once_with(f"Task with ID {args.task_id} updated.")

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    @patch('cli.interface.export_tasks')
    def test_handle_export_tasks_success(self, mock_export_tasks, mock_print, mock_create_storage):
        """
        Test exporting tasks to a file using the CLI interface.
        This test checks if the tasks are exported correctly and if the storage's list_tasks method is called.
        """
        mock_storage = MagicMock()
        mock_create_storage.return_value = mock_storage

        task1 = MagicMock()
        task1.id = 1
        task1.title = "Task 1"
        task1.description = "Description 1"
        task1.status.value = "completed"
        task1.created_at = datetime.now()
        task1.updated_at = datetime.now()
        task1.deadline = datetime.now() + timedelta(days=1)
       
        task2 = MagicMock()
        task2.id = 2
        task2.title = "Task 2"
        task2.description = "Description 2"
        task2.status.value = "pending"
        task2.created_at = datetime.now()
        task2.updated_at = datetime.now()
        task2.deadline = datetime.now() + timedelta(days=2)

        mock_storage.list_tasks.return_value = [task1, task2]

        args = MagicMock()
        args.storage_type = "memory"
        args.filename = "tasks.csv"
        args.format = "csv"

        handle_export_tasks(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_storage.list_tasks.assert_called_once_with()
        mock_export_tasks.assert_called_once_with([task1, task2], "tasks.csv", "csv")
        mock_print.assert_called_once_with(f"Tasks exported to tasks.csv in csv format.")

    @patch('cli.interface.StorageFactory.create_storage')
    @patch('cli.interface.print')
    @patch('cli.interface.logger')
    def test_handle_export_tasks_invalid_format(self, mock_logger, mock_print, mock_create_storage):
        """
        Test exporting tasks with an unsupported format.
        This test checks if the correct error message is printed when the format is unsupported.
        """
        mock_storage = MagicMock()
        mock_storage.list_tasks.return_value = []
        mock_create_storage.return_value = mock_storage

        args = MagicMock()
        args.storage_type = "memory"
        args.filename = "tasks.txt"
        args.format = "txt"

        with self.assertRaises(ValueError):
            handle_export_tasks(args)

        mock_create_storage.assert_called_once_with("memory")
        mock_print.assert_called_once_with("Error exporting tasks: Unsupported format: txt")
        mock_logger.error.assert_called_once_with("Error exporting tasks: Unsupported format: txt")

if __name__ == '__main__':
    unittest.main()