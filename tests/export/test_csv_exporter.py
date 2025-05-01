import unittest
import os
import csv
from datetime import datetime, timedelta
from models.task import Task, TaskStatus
from export.csv_exporter import export_tasks_to_csv

class TestCSVExporter(unittest.TestCase):
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
        self.filename = "test_tasks.csv"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_export_tasks_to_csv(self):
        export_tasks_to_csv(self.tasks, self.filename)

        self.assertTrue(os.path.exists(self.filename))

        with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['ID', 'Title', 'Description', 'Status', 'Created At', 'Updated At', 'Deadline'])

            for i, row in enumerate(reader):
                task = self.tasks[i]
                self.assertEqual(row[0], str(task.id))
                self.assertEqual(row[1], task.title)
                self.assertEqual(row[2], task.description)
                self.assertEqual(row[3], task.status.value)
                self.assertEqual(row[4], task.created_at.isoformat())
                self.assertEqual(row[5], task.updated_at.isoformat())
                self.assertEqual(row[6], task.deadline.isoformat() if task.deadline else "")

if __name__ == '__main__':
    unittest.main()

