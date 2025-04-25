from export import csv_exporter, markdown_exporter, json_exporter
from core.config import Config

exporters = {
    'csv': csv_exporter.export_tasks_to_csv,
    'json': json_exporter.export_tasks_to_json,
    'markdown': markdown_exporter.export_tasks_to_markdown,
}

def export_tasks(tasks, filename, format):
    """Export tasks to a file in the specified format.

    Args:
        tasks (list): List of Task objects to export.
        filename (str): The name of the file to write to.
        format (str): The format to export to ('csv', 'json', 'markdown').
    """
    # config = Config()
    # storage_type = config.storage_type

    if format not in exporters:
        raise ValueError(f"Unsupported format: {format}")

    exporter = exporters[format]
    exporter(tasks, filename)

    return filename