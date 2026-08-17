from fastapi import APIRouter, Depends, HTTPException

from models.task_model import Task, TaskResponse, TaskSingleResponse, TaskListResponse
from repositories.task_repository import TaskRepository, TaskManager, TaskManagerDict, TaskManagerSQLite
from services.task_service import TaskService
from auth.security import get_current_user

router = APIRouter()

manager = TaskManagerSQLite()

def get_repository():
    return manager

def get_service(repo: TaskRepository = Depends(get_repository)):
    return TaskService(repo)

@router.get("/")
def root():
    return {"status": "ok"}


@router.get("/tasks", response_model= TaskListResponse)
def get_tasks (service: TaskService = Depends(get_service)):
    
    tasks = service.get_tasks()

    return {
        "data": tasks,
        "error": None
    }

@router.post("/tasks", response_model= TaskSingleResponse)
def add_task(
             task: Task,
             service: TaskService = Depends(get_service),
             current_user: str = Depends(get_current_user)):

    
    new_task = service.create_task(task.title)

    return  {
        "data": new_task,
        "error": None
    }

@router.put("/tasks/{task_id}", response_model= TaskSingleResponse)
def update_task(
    task_id: int,
    service : TaskService = Depends(get_service),
    current_user: str = Depends(get_current_user)
    ):

    updated_task = service.toggle_task(task_id)

    if updated_task is None:
        raise HTTPException(status_code=404, detail=("Task not found"))

        
    
    return {
        "data": updated_task,
        "error": None
    }


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_service),
    current_user: str = Depends(get_current_user)
    ):

    deleted_task = service.delete_task(task_id)

    if deleted_task is None:
        raise HTTPException(status_code=404, detail= ("Task not found"))

    return {
        "data": deleted_task,
        
    }