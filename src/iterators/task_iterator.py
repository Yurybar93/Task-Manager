from datetime import datetime
from enum import Enum
from typing import List
from models.task import Task

class TaskIterator:
    """
    An iterator for filtering tasks based on various criteria.
    """
    def __init__(self, tasks: List[Task]) -> None:
        """
        Initialize the TaskIterator with a list of tasks.
        """
        self.tasks = tasks
        self.index = 0
        self.filters = []

    def __iter__(self):
        """
        Return the iterator object itself.
        """
        return self

    def __next__(self):
        """
        Return the next task that matches all filters.
        If no more tasks are available, raise StopIteration.
        """
        while self.index < len(self.tasks):
            task = self.tasks[self.index]
            self.index += 1
            if all(f(task) for f in self.filters):
                return task
        raise StopIteration

    def filter_by_status(self, status: str) -> 'TaskIterator':
        """
        Filter tasks by their status.
        Parameters:
        ----------
        status : str
            The status to filter tasks by. This can be a string representation of the status.
            It will be converted to lowercase for case-insensitive comparison.
        """
        status = status.strip().lower()
        
        def match(task):
            actual_status = task.status.value if isinstance(task.status, Enum) else str(task.status)
            return actual_status.lower() == status
        
        self.filters.append(match)
        return self

    def filter_by_deadline(self, deadline: datetime) -> 'TaskIterator':
        """
        Filter tasks by their deadline.
        Parameters:
        ----------
        deadline : datetime
            The deadline to filter tasks by. Only tasks with a deadline greater than or equal to this date will be included.
        """

        self.filters.append(lambda task: (task.deadline is not None and task.deadline >= deadline))
        return self 
