from models.task import Task, TaskStatus
from factory.storage_factory import StorageFactory
from datetime import datetime
from core.logger import Logger

logger = Logger()
log_action = logger.log_action

@log_action("Add task")
def handle_add_task(args):
    print(f"Received args: {args}")
    deadline = datetime.strptime(args.deadline, '%Y-%m-%d %H:%M:%S') if args.deadline else None
    task = Task(title=args.title, description=args.description, deadline=deadline)
    storage = StorageFactory.create_storage(args.storage_type)
    storage.add_task(task)
    print(f"Task '{task.title}' added with ID: {task.id}")

@log_action("Get task")
def handle_get_task(args):
    storage = StorageFactory.create_storage(args.storage_type)
    task = storage.get_task(args.task_id)
    if task:
        print(f"Task found: {task}")
    else:
        print(f"Task with ID {args.task_id} not found.")

@log_action("Delete task")
def handle_delete_task(args):
    storage = StorageFactory.create_storage(args.storage_type)
    if storage.delete_task(args.task_id):
        print(f"Task with ID {args.task_id} deleted.")
    else:
        print(f"Task with ID {args.task_id} not found.")        

@log_action("List tasks")
def handle_list_tasks(args):
    storage = StorageFactory.create_storage(args.storage_type)
    tasks = storage.list_tasks()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("No tasks found.")

@log_action("Update task")
def handle_update_task(args):
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
    else:
        print(f"Task with ID {args.task_id} not found.")