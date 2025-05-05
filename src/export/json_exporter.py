import json
from typing import List
from models.task import Task

def export_tasks_to_json(tasks: List[Task], filename: str) -> None:
    """
    Export tasks to a JSON file.
    Parameters:
    ----------
    tasks : List[Task]
        A list of Task objects to be exported.
    filename : str
        The name of the JSON file to which the tasks will be exported.

    Raises:
    --------
        IOError
            If there is an error writing to the file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"Error writing to file {filename}: {e}")
        