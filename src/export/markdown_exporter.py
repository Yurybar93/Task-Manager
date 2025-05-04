from typing import List
from models.task import Task

def export_tasks_to_markdown(tasks: List[Task], filename: str) -> None: 
    """Export tasks to a Markdown file.
    Parameters:
    ----------
    tasks : List[Task]
        A list of Task objects to be exported.
    filename : str
        The name of the Markdown file to which the tasks will be exported.

    Raises:
    --------
        IOError
            If there is an error writing to the file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("# Task List\n\n")
        file.write("| ID | Title | Description | Status | Created At | Updated At | Deadline |\n")
        file.write("|--------------------|-------|-------------|--------|------------|------------|----------|\n")
        
        for task in tasks:
            file.write(f"| {task.id} | {task.title} | {task.description} | {task.status.value} | "
                       f"{task.created_at.isoformat()} | {task.updated_at.isoformat()} | "
                       f"{task.deadline.isoformat() if task.deadline else ''} |\n")