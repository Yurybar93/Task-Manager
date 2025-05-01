import unittest
from storage.memory import MemoryStorage
from models.task import Task, TaskStatus

class TestMemoryStorage(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()

    def test_add_task(self):
        task = Task(title="Test Task", description="This is a test task.")
        self.storage.add_task(task)
        self.assertEqual(len(self.storage.tasks), 1)
        self.assertEqual(self.storage.tasks[0].title, "Test Task")

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
        self.assertEqual(len(self.storage.tasks), 0)

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