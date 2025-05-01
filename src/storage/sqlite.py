import sqlite3
from typing import List, Optional
from models.task import Task, TaskStatus
from storage.base import BaseStorage    
from datetime import datetime
from uuid import UUID


class SQLiteStorage(BaseStorage):
    def __init__(self, db_name: str = 'tasks.db'):
        self.connection = sqlite3.connect(db_name)
        self.db_name = db_name
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                deadline TEXT
            )
        ''')
        self.connection.commit()

    def add_task(self, task: Task) -> None:
        self.cursor.execute('''
            INSERT INTO tasks (id, title, description, status, created_at, updated_at, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(task.id), task.title, task.description, task.status.value, task.created_at.isoformat(), 
              task.updated_at.isoformat(), task.deadline.isoformat() if task.deadline else None))
        self.connection.commit()

    def get_task(self, task_id: str) -> Optional[Task]:
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = self.cursor.fetchone()
        if row:
            return Task(
                id=UUID(row[0]),
                title=row[1],
                description=row[2],
                status=TaskStatus[row[3].upper()],
                created_at=datetime.fromisoformat(row[4]),
                updated_at=datetime.fromisoformat(row[5]),
                deadline=datetime.fromisoformat(row[6]) if row[6] else None,
            )
        return None
    
    def delete_task(self, task_id: str) -> bool:
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_task(self, task: Task) -> bool:
        self.cursor.execute('''
            UPDATE tasks SET title = ?, description = ?, status = ?, updated_at = ?, deadline = ? WHERE id = ?
        ''', (task.title, task.description, task.status.value, task.updated_at.isoformat(), task.deadline, str(task.id)))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def list_tasks(self) -> List[Task]:
        self.cursor.execute('SELECT * FROM tasks')
        rows = self.cursor.fetchall()
        return [Task.from_db(row) for row in rows]