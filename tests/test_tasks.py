from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task_without_token():
    response = client.post("/tasks", json={"title": "tarea de prueba"})
    assert response.status_code == 401