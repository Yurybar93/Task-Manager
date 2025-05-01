import unittest
from storage.sqlite import SQLiteStorage
from models.task import Task, TaskStatus
from datetime import datetime
from uuid import uuid4

class TestSQLiteStorage(unittest.TestCase):
    def setUp(self):
        self.storage = SQLiteStorage(':memory:')  

    def test_add_task(self):
        task = Task(title="Test Task", description="This is a test task.")
        self.storage.add_task(task)
        retrieved_task = self.storage.get_task(str(task.id))
        self.assertEqual(retrieved_task.title, "Test Task")

    def test_get_task(self):
        task = Task(title="Test Task", description="This is a test task.")
        self.storage.add_task(task)
        retrieved_task = self.storage.get_task(str(task.id))
        self.assertEqual(retrieved_task.title, "Test Task")

    def test_delete_task(self):
        task = Task(title="Test Task", description="This is a test task.")
        self.storage.add_task(task)
        result = self.storage.delete_task(str(task.id))
        self.assertTrue(result)
        retrieved_task = self.storage.get_task(str(task.id))
        self.assertIsNone(retrieved_task)

    def test_update_task(self):
        task = Task(title="Test Task", description="This is a test task.")
        self.storage.add_task(task)
        task.title = "Updated Task"
        result = self.storage.update_task(task)
        self.assertTrue(result)
        updated_task = self.storage.get_task(str(task.id))
        self.assertEqual(updated_task.title, "Updated Task")

    def test_list_tasks(self):
        task1 = Task(title="Task 1", description="First task")
        task2 = Task(title="Task 2", description="Second task")
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        tasks = self.storage.list_tasks()
        self.assertEqual(len(tasks), 2)

if __name__ == '__main__':
    unittest.main()