import sqlite3
from database.database import get_connection

class TaskRepository:
    def create(self, title):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def toggle(self, task_id):
        raise NotImplementedError

    def delete(self, task_id):
        raise NotImplementedError

class TaskManager(TaskRepository):
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def _title_exists(self, title):
        for task in self.tasks:
            if task["title"] == title:
                return True
        return False

    def _find_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def create(self, title):

        if self._title_exists(title):
            raise ValueError("Title cannot be duplicate")

        new_task = {
            "id": self.next_id,
            "title": title,
            "done": False
        }

        self.tasks.append(new_task)
        self.next_id += 1
        return "ok"

    def get_all(self):
        return self.tasks

    def toggle(self, task_id):
        task = self._find_by_id(task_id)
        if not task:
            return False
        
        task["done"] = not task["done"]
        return True

class TaskManagerDict(TaskRepository):
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def create(self, title):

        for task in self.tasks.values():
            if task["title"] == title:
                raise ValueError("Title cannot be duplicate")

        new_task = {
            "id": self.next_id,
            "title": title,
            "done": False
        }

        self.tasks[self.next_id] = new_task
        self.next_id += 1
        return "ok"

    def get_all(self):
        return list(self.tasks.values())

    def toggle(self, task_id):
        task = self.tasks.get(task_id)
        if not task:
            return False

        task["done"] = not task["done"]
        return True
    
class TaskManagerSQLite(TaskRepository):
    def create(self, title):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                (title, False)
            )
            conn.commit()

            task_id = cursor.lastrowid

            return {"id": task_id,
                    "title":title,
                    "done":False
                }
        
        except sqlite3.IntegrityError:
            raise
        
        finally:
            conn.close()
        
    

    def get_all(self):

        conn = get_connection()
        cursor = conn.cursor()

        

        cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()

        conn.close()

        tasks = []

        for row in rows:
            tasks.append({
                "id": row[0],
                "title": row[1],
                "done": bool(row[2])
            })

        

        return tasks


    def toggle(self, task_id):
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT done FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()

        if not row:
            conn.close()
            return None
        
        current_value = bool(row[0])
        new_value = not current_value

        cursor.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (new_value, task_id)
        )

        conn.commit()

        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,)
        )

        updated_row= cursor.fetchone()

        conn.close()

        return {
            "id": updated_row[0],
            "title": updated_row[1],
            "done": bool(updated_row[2])
        }

    def delete(self, task_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT done FROM tasks WHERE id = ?",
            (task_id,)
        )

        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        conn.commit()
        conn.close()

        return {
            "status":"done",
            "error": None
        }