from export import csv_exporter, markdown_exporter, json_exporter
from typing import List
from models.task import Task

exporters = {
    'csv': csv_exporter.export_tasks_to_csv,
    'json': json_exporter.export_tasks_to_json,
    'markdown': markdown_exporter.export_tasks_to_markdown,
}

def export_tasks(tasks: List[Task], filename: str, format: str) -> str:
    """Export tasks to a file in the specified format.

    Parameters:
    ----------  
    tasks : list
        A list of Task objects to be exported.
    filename : str
        
    Returns:
    --------
        The name of the file to which the tasks were exported.

    Raises:
    --------
        ValueError: If the format is not supported.

    """


    if format not in exporters:
        raise ValueError(f"Unsupported format: {format}")

    exporter = exporters[format]
    exporter(tasks, filename)

    return filename