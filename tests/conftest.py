import os
from dotenv import load_dotenv

load_dotenv()

test_url = os.environ.get("TEST_DATABASE_URL")

if not test_url or "test" not in test_url:
    raise RuntimeError("TEST_DATABASE_URL no existe o no apunta a una base de prueba ")

os.environ["DATABASE_URL"]=test_url

import pytest
from database.database import get_connection, release_connection


@pytest.fixture(autouse=True)
def clean_database():
    yield
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE tasks, users RESTART IDENTITY;")
        conn.commit()
    finally:
        release_connection(conn)