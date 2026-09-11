from database.database import get_connection

class TaskRepository:
    def create(self, title, owner):
        raise NotImplementedError

    def get_all(self, owner):
        raise NotImplementedError

    def toggle(self, task_id, owner):
        raise NotImplementedError

    def delete(self, task_id, owner ):
        raise NotImplementedError
    
class TaskManagerSQLite(TaskRepository):
    def create(self, title, owner):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO tasks (title, done, owner) VALUES (?, ?, ?)",
                (title, False, owner)
            )
            conn.commit()

            task_id = cursor.lastrowid

            return {"id": task_id,
                    "title":title,
                    "done":False
                }
        
        
        finally:
            conn.close()
        
    

    def get_all(self, owner):

        conn = get_connection()
        cursor = conn.cursor()

        

        cursor.execute("SELECT * FROM tasks WHERE owner =?", (owner, ))

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


    def toggle(self, task_id, owner):
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT done FROM tasks WHERE id = ? AND owner = ?",
            (task_id, owner)
        )

        row = cursor.fetchone()

        if not row:
            conn.close()
            return None
        
        current_value = bool(row[0])
        new_value = not current_value

        cursor.execute(
            "UPDATE tasks SET done = ? WHERE id = ? AND owner = ?",
            (new_value, task_id, owner)
        )

        conn.commit()

        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = ? AND owner = ?",
            (task_id, owner)
        )

        updated_row= cursor.fetchone()

        conn.close()

        return {
            "id": updated_row[0],
            "title": updated_row[1],
            "done": bool(updated_row[2])
        }

    def delete(self, task_id, owner):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT done FROM tasks WHERE id = ? AND owner = ?",
            (task_id, owner)
        )

        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND owner = ?",
            (task_id, owner)
        )

        conn.commit()
        conn.close()

        return {
            "status":"done",
            "error": None
        }