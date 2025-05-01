import unittest
from datetime import datetime, timedelta
from uuid import uuid4, UUID
from models.task import Task, TaskStatus

class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(
            title="Test Task",
            description="This is a test task.",
            status=TaskStatus.PENDING,
            deadline=datetime.now() + timedelta(days=1)
        )

    def test_initialization(self):
        self.assertIsInstance(self.task.id, UUID)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task.")
        self.assertEqual(self.task.status, TaskStatus.PENDING)
        self.assertIsInstance(self.task.created_at, datetime)
        self.assertIsInstance(self.task.updated_at, datetime)

    def test_repr(self):
        expected_repr = f"Task(id={self.task.id}, title={self.task.title}, status={self.task.status}, created_at={self.task.created_at}, updated_at={self.task.updated_at})"
        self.assertEqual(repr(self.task), expected_repr)

    def test_str(self):
        deadline_str = self.task.deadline.strftime('%Y-%m-%d %H:%M:%S') if self.task.deadline else "No deadline"
        expected_str = (
            f"Task: {self.task.title}, Description: {self.task.description}, Status: ⏳ Pending, "
            f"Created at: {self.task.created_at.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"Updated at: {self.task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"Deadline: {deadline_str}"
        )
        self.assertEqual(str(self.task), expected_str)

    def test_mark_as_done(self):
        self.task.mark_as_done()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        self.assertTrue((datetime.now() - self.task.updated_at).total_seconds() < 1)

    def test_update_description(self):
        new_description = "Updated description."
        self.task.update_description(new_description)
        self.assertEqual(self.task.description, new_description)
        self.assertTrue((datetime.now() - self.task.updated_at).total_seconds() < 1)

    def test_is_overdue(self):
        self.task.deadline = datetime.now() - timedelta(days=1)
        self.assertTrue(self.task.is_overdue())
        self.task.status = TaskStatus.COMPLETED
        self.assertFalse(self.task.is_overdue())

    def test_to_dict(self):
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict["id"], str(self.task.id))
        self.assertEqual(task_dict["title"], self.task.title)
        self.assertEqual(task_dict["description"], self.task.description)
        self.assertEqual(task_dict["status"], self.task.status.value)
        self.assertEqual(task_dict["created_at"], self.task.created_at.isoformat())
        self.assertEqual(task_dict["updated_at"], self.task.updated_at.isoformat())
        self.assertEqual(task_dict["deadline"], self.task.deadline.isoformat())

    def test_from_dict(self):
        data = self.task.to_dict()
        new_task = Task.from_dict(data)
        self.assertIsInstance(new_task.id, UUID)
        self.assertEqual(new_task.title, data["title"])
        self.assertEqual(new_task.description, data["description"])
        self.assertEqual(new_task.status, TaskStatus[data["status"].upper()])
        self.assertEqual(new_task.created_at.isoformat(), data["created_at"])   
        self.assertEqual(new_task.updated_at.isoformat(), data["updated_at"])
        self.assertEqual(new_task.deadline.isoformat(), data["deadline"]) 

    def test_from_db(self):
        row = (
            str(self.task.id),
            self.task.title,
            self.task.description,  
            self.task.status.value,
            self.task.created_at.isoformat(),
            self.task.updated_at.isoformat(),
            self.task.deadline.isoformat()
        )
        task_from_db = Task.from_db(row)

        self.assertEqual(task_from_db.id, self.task.id) 
        self.assertEqual(task_from_db.title, self.task.title)  
        self.assertEqual(task_from_db.description, self.task.description)  
        self.assertEqual(task_from_db.status, self.task.status)  
        self.assertEqual(task_from_db.created_at, self.task.created_at)  
        self.assertEqual(task_from_db.updated_at, self.task.updated_at) 
        self.assertEqual(task_from_db.deadline, self.task.deadline) 

if __name__ == "__main__":
    unittest.main()