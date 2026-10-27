from psycopg2.pool import ThreadedConnectionPool
from config.config import settings

pool = ThreadedConnectionPool(minconn=1, maxconn=10, dsn=settings.database_url)


def get_connection():
    return pool.getconn()

def release_connection(conn):
    pool.putconn(conn)



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
    CREATE INDEX IF NOT EXISTS idx_tasks_owner ON tasks (owner);
""")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY ,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        
    """)

    conn.commit()
    release_connection(conn)