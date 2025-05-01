from storage.base import BaseStorage    
from models.task import Task
from typing import List, Optional

class MemoryStorage(BaseStorage):
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if str(task.id) == task_id:
                return task
        return None

    def delete_task(self, task_id: str) -> bool:
        for i, task in enumerate(self.tasks):
            if str(task.id) == task_id:
                del self.tasks[i]
                return True
        return False

    def list_tasks(self) -> List[Task]:
        return self.tasks.copy()

    def update_task(self, task: Task) -> bool:
        for i, existing_task in enumerate(self.tasks):
            if str(existing_task.id) == str(task.id):
                self.tasks[i] = task
                return True
        return False