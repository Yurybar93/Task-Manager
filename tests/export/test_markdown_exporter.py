import unittest
import os
from datetime import datetime, timedelta
from uuid import UUID
from models.task import Task, TaskStatus
from export.markdown_exporter import export_tasks_to_markdown

class TestMarkdownExporter(unittest.TestCase):
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
        self.filename = "test_tasks.md"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_export_tasks_to_markdown(self):
        export_tasks_to_markdown(self.tasks, self.filename)

        self.assertTrue(os.path.exists(self.filename))

        with open(self.filename, mode='r', encoding='utf-8') as file:
            content = file.read()
            for task in self.tasks:
                self.assertIn(task.title, content)
                self.assertIn(task.description, content)
                self.assertIn(task.status.value, content)
                self.assertIn(task.created_at.isoformat(), content)
                self.assertIn(task.updated_at.isoformat(), content)
                if task.deadline:
                    self.assertIn(task.deadline.isoformat(), content)

        if __name__ == '__main__':
            unittest.main()   