from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from argparse import Namespace
from cli.interface import handle_add_task, handle_get_task, handle_delete_task, handle_list_tasks, handle_update_task, handle_export_tasks
from core.config import Config
import uvicorn
from models.task import TaskStatus 

config = Config()
app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: Optional[str] = None
    storage_type: Optional[str] = config.storage_type

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[str] 
    storage_type: Optional[str] 
    status: Optional[str] 

@app.post("/tasks/add", status_code=201)
def add_task(task: TaskCreate):
    """
    Add a new task to the storage.
    """
    args = Namespace(title=task.title, description=task.description, deadline=task.deadline, storage_type=task.storage_type)
    return handle_add_task(args)

@app.get("/tasks/export")
def export_tasks(filename: str, format: str, storage_type: Optional[str] = config.storage_type):
    """
    Export tasks to a file.
    """
    args = Namespace(filename=filename, format=format, storage_type=storage_type)
    return handle_export_tasks(args)

@app.get("/tasks/{task_id}")
def get_task(task_id: str, storage_type: Optional[str] = config.storage_type):
    """
    Get a task by its ID.
    """
    args = Namespace(task_id=task_id, storage_type=storage_type)
    task = handle_get_task(args)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, storage_type: Optional[str] = config.storage_type):
    """
    Delete a task by its ID.
    """
    args = Namespace(task_id=task_id, storage_type=storage_type)
    return handle_delete_task(args)

@app.get("/tasks")
def list_tasks(storage_type: Optional[str] = config.storage_type, status: Optional[str] = None, deadline: Optional[str] = None):
    """
    List all tasks.
    """
    args = Namespace(storage_type=storage_type, status=status, deadline=deadline)
    return handle_list_tasks(args)

@app.put("/tasks/update/{task_id}")
def update_task(task_id: str, task: TaskUpdate, storage_type: Optional[str] = config.storage_type):
    """
    Update a task by its ID.
    """
    args = Namespace(task_id=task_id, title=task.title, description=task.description, status=task.status, storage_type=storage_type, deadline=task.deadline)
    return handle_update_task(args)



@app.get("/")
def read_root():
    return {"message": "Task Manager API is running. Visit /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run("api:app")
    