import csv
from typing import List
from models.task import Task

def export_tasks_to_csv(tasks: List[Task], filename: str) -> None:
    """Export tasks to a CSV file.

    Args:
        tasks (List[Task]): List of Task objects to export.
        filename (str): The name of the CSV file to write to.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['ID', 'Title', 'Description', 'Status', 'Created At', 'Updated At', 'Deadline'])
        
        # Write task data
        for task in tasks:
            writer.writerow([
                str(task.id),
                task.title,
                task.description,
                task.status.value,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.deadline.isoformat() if task.deadline else ""
            ])