from models.task import Task, TaskStatus
from factory.storage_factory import StorageFactory
from datetime import datetime
from core.logger import Logger
from iterators.task_iterator import TaskIterator 
from export.export import export_tasks   

logger = Logger()
log_action = Logger.log_action

@log_action("Add task")
def handle_add_task(args):
    """
    Handle the addition of a new task.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - title : str
        - description : str
        - deadline : str (optional, format: YYYY-MM-DD HH:MM:SS)
        - storage_type : str (optional, default: 'jsonfile')

"""
    print(f"Received args: {args}")
    deadline = datetime.strptime(args.deadline, '%Y-%m-%d %H:%M:%S') if args.deadline else None
    task = Task(title=args.title, description=args.description, deadline=deadline)
    storage = StorageFactory.create_storage(args.storage_type)
    storage.add_task(task)
    print(f"Task '{task.title}' added with ID: {task.id}")
    return task

@log_action("Get task")
def handle_get_task(args):
    """
    Handle the retrieval of a task by its ID.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - task_id : str
        - storage_type : str (optional, default: 'jsonfile')
    """
    storage = StorageFactory.create_storage(args.storage_type)
    task = storage.get_task(args.task_id)
    if task:
        print(f"Task found: {task}")
        return task
    else:
        print(f"Task with ID {args.task_id} not found.")

@log_action("Delete task")
def handle_delete_task(args):
    """
    Handle the deletion of a task by its ID.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - task_id : str
        - storage_type : str (optional, default: 'jsonfile')
    """
    storage = StorageFactory.create_storage(args.storage_type)
    if storage.delete_task(args.task_id):
        print(f"Task with ID {args.task_id} deleted.")
    else:
        print(f"Task with ID {args.task_id} not found.")        

@log_action("List tasks")
def handle_list_tasks(args):
    """
    Handle the listing of tasks with optional filters.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - status : str (optional, filter by task status)
        - deadline : str (optional, filter by task deadline, format: YYYY-MM-DD HH:MM:SS)
        - storage_type : str (optional, default: 'jsonfile')
    """
    storage = StorageFactory.create_storage(args.storage_type)
    tasks = storage.list_tasks()
    task_iterator = TaskIterator(tasks)

    if getattr(args, 'status', None):
        task_iterator = task_iterator.filter_by_status(args.status)

    if getattr(args, 'deadline', None):
        try:
            deadline = datetime.strptime(args.deadline, '%Y-%m-%d %H:%M:%S')
            print(f"Deadline for filtering: {deadline}")
            task_iterator = task_iterator.filter_by_deadline(deadline)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD HH:MM:SS")
            return

    any_tasks = False
    for task in task_iterator:
        print(task)
        any_tasks = True

    if not any_tasks:
        print("No tasks found.")

    return task_iterator.tasks  


@log_action("Update task")
def handle_update_task(args):
    """
    Handle the update of a task by its ID.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - task_id : str
        - title : str (optional)
        - description : str (optional)
        - status : str (optional, values: 'PENDING', 'COMPLETED', 'FAILED')
        - deadline : str (optional, format: YYYY-MM-DD HH:MM:SS)
        - storage_type : str (optional, default: 'jsonfile')
    """
    deadline = datetime.strptime(args.deadline, '%Y-%m-%d %H:%M:%S') if args.deadline else None
    storage = StorageFactory.create_storage(args.storage_type)
    task = storage.get_task(args.task_id)
    if task:
        if args.title:
            task.title = args.title
        if args.description:
            task.description = args.description
        if args.status:
            task.status = TaskStatus[args.status.upper()]
        if deadline:
            task.deadline = deadline
        storage.update_task(task)
        print(f"Task with ID {args.task_id} updated.")
        return task
    else:
        print(f"Task with ID {args.task_id} not found.")
        return None

@log_action("Export tasks")
def handle_export_tasks(args):
    """
    Handle the export of tasks to a file.
    Parameters:
    ----------
    args : Namespace
        The command line arguments parsed by argparse.
        - filename : str
        - format : str (optional, default: 'json', values: 'json', 'csv')
        - storage_type : str (optional, default: 'jsonfile')
    """
    try:
        storage = StorageFactory.create_storage(args.storage_type)
        tasks = storage.list_tasks()
        export_tasks(tasks, args.filename, args.format)
        print(f"Tasks exported to {args.filename} in {args.format} format.")
        return tasks
    except Exception as e:
        print(f"Error exporting tasks: {e}")
        logger.error(f"Error exporting tasks: {e}")
        raise e