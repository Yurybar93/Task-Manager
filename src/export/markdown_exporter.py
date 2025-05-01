from typing import List
from models.task import Task

def export_tasks_to_markdown(tasks: List[Task], filename: str) -> None: 
    """Export tasks to a Markdown file.

    Args:
        tasks (List[Task]): List of Task objects to export.
        filename (str): The name of the Markdown file to write to.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        # Write the header
        file.write("# Task List\n\n")
        file.write("| ID | Title | Description | Status | Created At | Updated At | Deadline |\n")
        file.write("|--------------------|-------|-------------|--------|------------|------------|----------|\n")
        
        # Write task data
        for task in tasks:
            file.write(f"| {task.id} | {task.title} | {task.description} | {task.status.value} | "
                       f"{task.created_at.isoformat()} | {task.updated_at.isoformat()} | "
                       f"{task.deadline.isoformat() if task.deadline else ''} |\n")