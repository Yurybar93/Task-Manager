import unittest
from fastapi.testclient import TestClient
from api import app

class TestAPI(unittest.TestCase):
    """
    Test case for the FastAPI application.
    """
    def setUp(self):
        """
        Set up the test case with a FastAPI test client.
        """
        self.client = TestClient(app)

    def test_add_task(self):
        """
        Test adding a new task to the storage.
        """
        response = self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_task(self):
        """
        Test getting a task by its ID.
        """       
        # First, add a task to get its ID
        add_response = self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        task_id = add_response.json()["id"]
        
        # Now, get the task by its ID
        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        print(response.text)
        self.assertEqual(response.json()["title"], "Test Task")

    def test_delete_task(self):
        """
        Test deleting a task by its ID.
        """
        # First, add a task to get its ID
        add_response = self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        task_id = add_response.json()["id"]
        
        # Now, delete the task by its ID
        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        
        # Verify that the task is deleted
        get_response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_list_tasks(self):  
        """
        Test listing all tasks.
        """
        # First, add a task to ensure there is at least one task in the storage
        self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        
        response = self.client.get("/tasks")
        tasks = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)
        self.assertIn("id", tasks[0])
        self.assertTrue(any(task["title"] == "Test Task" for task in tasks))

    def test_list_sorted_by_deadline(self):
        """
        Test listing tasks sorted by deadline.
        """
        # First, add tasks with deadlines
        self.client.post("/tasks/add", json={"title": "Task 1", "description": "This is a test task.", "deadline": "2025-05-01 10:00:00"})
        self.client.post("/tasks/add", json={"title": "Task 2", "description": "This is another test task.", "deadline": "2025-05-02 10:00:00"})
        self.client.post("/tasks/add", json={"title": "Task 3", "description": "This is a third test task.", "deadline": "2025-05-03 10:00:00"})
        
        response = self.client.get("/tasks?sort=deadline")
        tasks = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(tasks, list)
        self.assertTrue(all(tasks[i]['deadline'] <= tasks[i+1]['deadline'] for i in range(len(tasks)-1)))
        self.assertEqual(tasks[0]['title'], "Task 1")
        self.assertEqual(tasks[1]['title'], "Task 2")
        self.assertEqual(tasks[2]['title'], "Task 3")

    def test_list_sorted_by_status(self):
        """
        Test listing tasks sorted by status.
        """
        # First, add tasks with different statuses
        self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task.", "status": "completed"})
        self.client.post("/tasks/add", json={"title": "Another Task", "description": "This is another test task.", "status": "pending"})
        
        response = self.client.get("/tasks?sort=status")
        tasks = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(tasks, list)
        self.assertTrue(all(task['status'] == 'pending' for task in tasks))
        self.assertGreater(len(tasks), 0)

    def test_update_task(self):
        """
        Test updating a task by its ID.
        """
        # First, add a task to get its ID
        add_response = self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        task_id = add_response.json()["id"]
        
        # Now, update the task by its ID
        response = self.client.put(f"/tasks/update/{task_id}", json={"title": "Updated Task", "description": "This is an updated test task."})
        print(response.status_code)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Task")

    def test_export_tasks(self):
        """
        Test exporting tasks to a file.
        """
        # First, add a task to ensure there is at least one task in the storage
        self.client.post("/tasks/add", json={"title": "Test Task", "description": "This is a test task."})
        
        response = self.client.get("/tasks/export?filename=tasks.json&format=json")
        print("Response status:", response.status_code)
        print("Response json:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.headers["Content-Type"])
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)

    def tearDown(self):
        response = self.client.get("/tasks")
        tasks = response.json()
        for task in tasks:
            self.client.delete(f"/tasks/{task['id']}")

if __name__ == "__main__":
    unittest.main()