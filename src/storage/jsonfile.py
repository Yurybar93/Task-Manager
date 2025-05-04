import json
from typing import List, Optional
from models.task import Task
from storage.base import BaseStorage     

class JSONFileStorage(BaseStorage):
    """
    A class to manage task storage in a JSON file.
    This class implements the BaseStorage interface and provides methods
    to add, retrieve, delete, list, and update tasks in a JSON file.
    """
    def __init__(self, filename: str):
        """
        Initialize the JSONFileStorage with a filename.
        If the file does not exist or is empty, an empty task list is created.
        """
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the JSON file.
        If the file does not exist or is empty, return an empty list.
        """
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_tasks(self) -> None:
        """
        Save the current list of tasks to the JSON file.
        This method overwrites the existing file with the current task list.
        """
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, default=str)

    def add_task(self, task: Task) -> None:
        """
        Add a new task to the storage.
        This method appends the task to the current list and saves it to the file.
        """
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        If the task is found, return it; otherwise, return None.
        """
        for task in self.tasks:
            if str(task.id) == task_id:
                return task
        return None 
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID.
        If the task is found and deleted, return True; otherwise, return False.
        """
        for i, task in enumerate(self.tasks):
            if str(task.id) == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def update_task(self, task: Task) -> bool:
        """
        Update an existing task in the storage.
        If the task is found, it is updated and saved to the file.
        Return True if the task was updated; otherwise, return False.
        """
        for i, existing_task in enumerate(self.tasks):
            if str(existing_task.id) == str(task.id):
                self.tasks[i] = task
                self.save_tasks()
                return True
        return False
    
    def list_tasks(self) -> List[Task]:
        """
        List all tasks in the storage.
        This method returns a copy of the current task list.
        """
        return self.tasks.copy()