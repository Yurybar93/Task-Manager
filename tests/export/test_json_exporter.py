import unittest
import os
import json
from datetime import datetime, timedelta
from models.task import Task, TaskStatus
from export.json_exporter import export_tasks_to_json

class TestJSONExporter(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            Task(
                title="Test Task 1",
                description="This is the first test task.",
                status=TaskStatus.PENDING,
                deadline=datetime.now() + timedelta(days=1)
            ),
            Task(
                title="Test Task 2",
                description="This is the second test task.",
                status=TaskStatus.COMPLETED,
                deadline=datetime.now() - timedelta(days=1)
            )
        ]
        self.filename = "test_tasks.json"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_export_tasks_to_json(self):
        export_tasks_to_json(self.tasks, self.filename)

        self.assertTrue(os.path.exists(self.filename))

        with open(self.filename, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data), len(self.tasks))

            for i, task_data in enumerate(data):
                task = self.tasks[i]
                self.assertEqual(task_data["id"], str(task.id))
                self.assertEqual(task_data["title"], task.title)
                self.assertEqual(task_data["description"], task.description)
                self.assertEqual(task_data["status"], task.status.value)
                self.assertEqual(task_data["created_at"], task.created_at.isoformat())
                self.assertEqual(task_data["updated_at"], task.updated_at.isoformat())
                self.assertEqual(task_data["deadline"], task.deadline.isoformat() if task.deadline else None)

if __name__ == '__main__':
    unittest.main()