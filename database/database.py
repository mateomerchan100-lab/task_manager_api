from psycopg2.pool import ThreadedConnectionPool
from config.config import settings

pool = ThreadedConnectionPool(minconn=1, maxconn=10, dsn=settings.database_url)


def get_connection():
    return pool.getconn()

def release_connection(conn):
    pool.putconn(conn)

