import argparse
from cli.interface import handle_add_task, handle_get_task, handle_delete_task, handle_list_tasks, handle_update_task, handle_export_tasks
from core.config import Config

def main():
    """
    Main function to parse command line arguments and execute the corresponding task management command.
    It uses argparse to handle command line arguments and subcommands for adding, retrieving, deleting,
    listing, updating, and exporting tasks.
    
    Commands:
    - add: Add a new task
    - get: Retrieve a task by ID
    - delete: Delete a task by ID
    - list: List all tasks
    - update: Update a task by ID
    - export: Export tasks to a file

    Notes:
    - The `--storage_type` argument specifies the type of storage to use (memory, jsonfile, sqlite).
    """
    config = Config()
    parser = argparse.ArgumentParser(description="Task Management CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', type=str, help='Title of the task')
    add_parser.add_argument('description', type=str, help='Description of the task')
    add_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    add_parser.add_argument('--deadline', type=str, help='Deadline of the task (YYYY-MM-DD HH:MM:SS)')
    add_parser.set_defaults(func=handle_add_task)

    # Get task command
    get_parser = subparsers.add_parser('get', help='Get a task by ID')
    get_parser.add_argument('task_id', type=str, help='ID of the task to retrieve')
    get_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    get_parser.set_defaults(func=handle_get_task)

    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task by ID')
    delete_parser.add_argument('task_id', type=str, help='ID of the task to delete')
    delete_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    delete_parser.set_defaults(func=handle_delete_task)

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    list_parser.add_argument('--status', type=str, choices=['pending', 'completed'], help='Filter tasks by status')
    list_parser.add_argument('--deadline', type=str, help='Filter tasks by deadline (YYYY-MM-DD HH:MM:SS)')
    list_parser.set_defaults(func=handle_list_tasks)

    # Update task command
    update_parser = subparsers.add_parser('update', help='Update a task by ID')
    update_parser.add_argument('task_id', type=str, help='ID of the task to update')
    update_parser.add_argument('--title', type=str, help='New title for the task')
    update_parser.add_argument('--description', type=str, help='New description for the task')
    update_parser.add_argument('--status', type=str, choices=['pending', 'completed'], help='New status for the task')
    update_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    update_parser.add_argument('--deadline', type=str, help='New deadline for the task (YYYY-MM-DD HH:MM:SS)')
    update_parser.set_defaults(func=handle_update_task)

    # Export tasks command
    export_parser = subparsers.add_parser('export', help='Export tasks to a file') 
    export_parser.add_argument('filename', type=str, help='Name of the file to export to')
    export_parser.add_argument('format', type=str, choices=['csv', 'json', 'markdown'], help='Format to export to (csv, json, markdown)')   
    export_parser.add_argument('--storage_type', type=str, default=config.storage_type, help='Type of storage (memory, jsonfile, sqlite)')
    export_parser.set_defaults(func=handle_export_tasks)


    args = parser.parse_args()
    args.func(args)

    
if __name__ == '__main__':
    main()