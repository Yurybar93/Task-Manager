import json
from typing import List
from models.task import Task

def export_tasks_to_json(tasks: List[Task], filename: str) -> None:
    """Export tasks to a JSON file.

    Args:
        tasks (List[Task]): List of Task objects to export.
        filename (str): The name of the JSON file to write to.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)