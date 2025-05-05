from datetime import datetime
from enum import Enum

class TaskIterator:
    def __init__(self, tasks):
        self.tasks = tasks
        self.index = 0
        self.filters = []

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.tasks):
            task = self.tasks[self.index]
            self.index += 1
            if all(f(task) for f in self.filters):
                return task
        raise StopIteration

    def filter_by_status(self, status):
        status = status.strip().lower()
        
        def match(task):
            actual_status = task.status.value if isinstance(task.status, Enum) else str(task.status)
            return actual_status.lower() == status
        
        self.filters.append(match)
        return self

    def filter_by_deadline(self, deadline):
        self.filters.append(lambda task: (task.deadline is not None and task.deadline >= deadline))
        return self 
