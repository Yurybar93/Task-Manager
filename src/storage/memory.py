from storage.base import BaseStorage    
from models.task import Task
from typing import List, Optional

class MemoryStorage(BaseStorage):
    """
    A class to manage task storage in memory.
    This class implements the BaseStorage interface and provides methods
    to add, retrieve, delete, list, and update tasks in memory.
    """
    def __init__(self):
        """
        Initialize the MemoryStorage with an empty task list.
        """
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """
        Add a new task to the storage.
        This method appends the task to the current list.
        """
        self.tasks.append(task)

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
                return True
        return False

    def list_tasks(self) -> List[Task]:
        """
        List all tasks in the storage.
        Returns a copy of the current task list.
        """
        return self.tasks.copy()

    def update_task(self, task: Task) -> bool:
        """
        Update an existing task in the storage.
        If the task is found and updated, return True; otherwise, return False.
        """
        for i, existing_task in enumerate(self.tasks):
            if str(existing_task.id) == str(task.id):
                self.tasks[i] = task
                return True
        return False