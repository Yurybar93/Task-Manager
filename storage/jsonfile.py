import json
from typing import List, Optional
from models.task import Task
from storage.base import BaseStorage     

class JSONFileStorage(BaseStorage):
    def __init__(self, filename: str):
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    def save_tasks(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, default=str)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if str(task.id) == task_id:
                return task
        return None 
    
    def delete_task(self, task_id: str) -> bool:
        for i, task in enumerate(self.tasks):
            if str(task.id) == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def update_task(self, task):
        for i, existing_task in enumerate(self.tasks):
            if str(existing_task.id) == str(task.id):
                self.tasks[i] = task
                self.save_tasks()
                return True
        return False
    
    def list_tasks(self) -> List[Task]:
        return self.tasks.copy()