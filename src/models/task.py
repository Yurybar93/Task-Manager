from datetime import datetime
import uuid
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task:
    """
    A class representing a task with various attributes and methods to manipulate it.
    """
    def __init__(self, title: str, description: str,  status: TaskStatus = TaskStatus.PENDING, id = None, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, deadline: datetime = None):
        """
        Initializes a Task instance with the given attributes.
        Parameters:
        ----------
        title : str
            The title of the task.
        description : str
            A brief description of the task.
        status : TaskStatus, optional
            The status of the task (default is TaskStatus.PENDING).
        id : UUID, optional
            A unique identifier for the task (default is a new UUID).
        created_at : datetime, optional
            The date and time when the task was created (default is the current date and time).
        updated_at : datetime, optional
            The date and time when the task was last updated (default is the current date and time).
        deadline : datetime, optional
            The deadline for the task (default is None).
        """
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __repr__(self): 
        """
        Returns a string representation of the Task instance.
        """
        return f"Task(id={self.id}, title={self.title}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"
    
    def __str__(self):
        """
        Returns a formatted string representation of the Task instance.
        """
        status_icons = {
         "pending": "⏳",
        "completed": "✅"
        }
        status_display = f"{status_icons.get(self.status.value, '')} {self.status.value.capitalize()}"
        return (
                f"Task: {self.title}, Description: {self.description}, Status: {status_display}, " 
                f"Created at: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Updated at: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Deadline: {(self.deadline.strftime('%Y-%m-%d %H:%M:%S') if self.deadline else 'No deadline set')}"
                )
    
    def mark_as_done(self):
        """
        Marks the task as completed and updates the updated_at timestamp.
        """
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now()
        print(f"Task '{self.title}' marked as completed.")
    
    def update_description(self, new_description: str):
        """
        Updates the description of the task and updates the updated_at timestamp.
        Parameters:
        ----------
        new_description : str
            The new description for the task.
        """
        self.description = new_description
        self.updated_at = datetime.now()
        print(f"Task '{self.title}' description updated.")

    def is_overdue(self) -> bool:
        """
        Checks if the task is overdue based on the current date and time.
        Returns:
        -------
        bool
            True if the task is overdue, False otherwise.
        """
        return self.deadline is not None and datetime.now() > self.deadline and self.status != TaskStatus.COMPLETED
    
    def to_dict(self):
        """
        Converts the Task instance to a dictionary representation.
        Returns:
        -------
        dict
            A dictionary containing the task's attributes.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Task instance from a dictionary representation.
        Parameters:
        ----------
        data : dict
            A dictionary containing the task's attributes.
        Returns:
        -------
        Task
            A Task instance created from the dictionary data.
        """
        task = cls(
            title=data["title"],
            description=data["description"],
            status=TaskStatus[data["status"].upper()],
        )
        task.id = uuid.UUID(data["id"])
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])

        if "deadline" in data:
            task.deadline = datetime.fromisoformat(data["deadline"]) if isinstance(data["deadline"], str) else None
        else:
            task.deadline = None
        return task
    
    @classmethod
    def from_db(cls, row: tuple):
        """
        Creates a Task instance from a database row.
        Parameters:
        ----------
        row : tuple
            A tuple containing the task's attributes as returned from a database query.
        Returns:
        -------
        Task
            A Task instance created from the database row.
        """
        return cls(
            id=UUID(row[0]),
            title=row[1],
            description=row[2],
            status=TaskStatus[row[3].upper()],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5]),
            deadline=datetime.fromisoformat(row[6]) if row[6] else None,
        )

    