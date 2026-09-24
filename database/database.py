import psycopg2
from config.config import settings




def get_connection():
    conn = psycopg2.connect(settings.database_url)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY ,
        title TEXT NOT NULL UNIQUE,
        done BOOLEAN NOT NULL,
        owner TEXT NOT NULL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY ,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        
    """)

    conn.commit()
    conn.close()