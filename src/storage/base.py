from abc import ABC, abstractmethod
from typing import List
from models.task import Task

class BaseStorage(ABC):
    @abstractmethod
    def add_task(self, task: Task):
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def list_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def update_task(self, task: Task) -> bool:
        pass
