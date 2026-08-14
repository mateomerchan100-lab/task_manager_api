import sqlite3
from database.database import get_connection


class UserRepository:

    def create_user(self, username, password):
        raise NotImplementedError

    def find_by_username(self, username):
        raise NotImplementedError


class UserManagerSQLite(UserRepository):
    def create_user(self, username, password):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            return {"username":username}
        finally:
            conn.close()



    def find_by_username(self, username):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username =?",
                (username,)
        )

            found_user = cursor.fetchone()

            if not found_user:
                return None

            return{
                "id": found_user[0],
                "username": found_user[1],
                "password": found_user[2]
            }
            
        finally:
            conn.close()
        