from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task_without_token():
    response = client.post("/tasks", json={"title": "tarea de prueba"})
    assert response.status_code == 401


def test_update_task_not_found():
    response = client.post("/register", json={"username":"user1", "password": "password"})
    login_response = client.post("/login", data={"username": "user1", "password":"password"})
    token = login_response.json()["access_token"]
    response = client.put("/tasks/99999", headers={"Authorization":f"bearer {token}"})
    assert response.status_code == 404


def test_create_duplicate_task():
    response = client.post("/register", json={"username":"user2", "password": "password"})
    login_response = client.post("/login", data={"username":"user2", "password": "password"})
    token = login_response.json()["access_token"]
    first_response = client.post("/tasks", json= {"title": "Unique_test_002"}, headers={"Authorization":f"bearer {token}"}) #modificar "title" en cada uso debido a la existencia de la tarea
    second_response = client.post("/tasks", json= {"title": "Unique_test_002"}, headers={"Authorization":f"bearer {token}"}) #modificar "title" en cada uso debido a la existencia de la tarea

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_delete_task():
    response = client.post("/register", json={"username":"user_delete", "password":"password"})
    login_response = client.post("/login",data={"username":"user_delete","password":"password"} )
    token = login_response.json()["access_token"]
    create_task = client.post("/tasks", json={"title":"Task_to_delete_002"}, headers={"Authorization":f"bearer {token}"}) #Modify Task number between requests
    task_id = create_task.json()["data"]["id"]
    first_delete = client.delete(f"/tasks/{task_id}", headers={"Authorization":f"bearer {token}"}) 
    second_delete = client.delete(f"/tasks/{task_id}", headers={"Authorization":f"bearer {token}"}) 

    assert first_delete.status_code == 200 
    assert second_delete.status_code == 404


    