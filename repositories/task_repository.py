from database.database import get_connection, release_connection

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
                "INSERT INTO tasks (title, done, owner) VALUES (%s, %s, %s) RETURNING id",
                (title, False, owner)
            )
            conn.commit()

            task_id = cursor.fetchone()[0]

            return {"id": task_id,
                    "title":title,
                    "done":False
                }
        
        
        finally:
            release_connection(conn)
        
    

    def get_all(self, owner):
        
        conn = get_connection()
        try:

            cursor = conn.cursor()

        
            cursor.execute("SELECT * FROM tasks WHERE owner = %s", (owner, ))

            rows = cursor.fetchall()

        finally: 
            release_connection(conn)

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
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT done FROM tasks WHERE id = %s AND owner = %s",
                (task_id, owner)
            )

            row = cursor.fetchone()

            if not row:
                return None
            
            current_value = bool(row[0])
            new_value = not current_value

            cursor.execute(
                "UPDATE tasks SET done = %s WHERE id = %s AND owner = %s",
                (new_value, task_id, owner)
            )

            conn.commit()

            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s AND owner = %s",
                (task_id, owner)
            )

            updated_row = cursor.fetchone()

        finally:
            release_connection(conn)

        return {
            "id": updated_row[0],
            "title": updated_row[1],
            "done": bool(updated_row[2])
        }

    def delete(self, task_id, owner):

        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT done FROM tasks WHERE id = %s AND owner = %s",
                (task_id, owner)
            )

            row = cursor.fetchone()

            if not row:
                return None

            cursor.execute(
                "DELETE FROM tasks WHERE id = %s AND owner = %s",
                (task_id, owner)
            )

            conn.commit()
        finally:
            release_connection(conn)

        return {
            "status":"done",
            "error": None
        }