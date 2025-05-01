import unittest
from datetime import datetime, timedelta
from uuid import uuid4
from models.task import Task, TaskStatus
from iterators.task_iterator import TaskIterator

class TestTaskIterator(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            Task(id=uuid4(), title="Task 1", description="First task", status=TaskStatus.PENDING, created_at=datetime.now(), updated_at=datetime.now(), deadline=datetime.now() + timedelta(days=1)),
            Task(id=uuid4(), title="Task 2", description="Second task", status=TaskStatus.COMPLETED, created_at=datetime.now(), updated_at=datetime.now(), deadline=datetime.now() + timedelta(days=2)),
            Task(id=uuid4(), title="Task 3", description="Third task", status=TaskStatus.COMPLETED, created_at=datetime.now(), updated_at=datetime.now(), deadline=None),
        ]
        self.iterator = TaskIterator(self.tasks)

    def test_iterate_tasks(self):
        iterator = TaskIterator(self.tasks)
        task_list = list(iterator)
        self.assertEqual(len(task_list), len(self.tasks))

    def test_filter_by_status(self):
        iterator = TaskIterator(self.tasks)
        iterator.filter_by_status("pending")
        filtered_tasks = list(iterator)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].status, TaskStatus.PENDING)

    def test_filter_by_deadline(self):
        deadline = datetime.now() + timedelta(days=1)
        task_with_deadline = Task(id=uuid4(), title="Task with deadline", description="This task has a deadline", status=TaskStatus.COMPLETED, created_at=datetime.now(), updated_at=datetime.now(), deadline=deadline)
        self.tasks.append(task_with_deadline)
        iterator = TaskIterator(self.tasks)
        iterator.filter_by_deadline(datetime.now())
        filtered_tasks = list(iterator)
        self.assertIn(task_with_deadline, filtered_tasks)

    def test_chained_filters(self):
        iterator = TaskIterator(self.tasks)
        iterator.filter_by_status("completed").filter_by_deadline(datetime.now())
        filtered_tasks = list(iterator)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0].status, TaskStatus.COMPLETED)

    if __name__ == '__main__':
        unittest.main()