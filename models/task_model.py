from pydantic import BaseModel, Field
from typing import Optional, List

class Task(BaseModel):
    title : str = Field(min_length=1)


class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool


class TaskSingleResponse(BaseModel):
    data: TaskResponse | None
    error: str | None

class TaskListResponse(BaseModel):
    data: list[TaskResponse] | None
    error: str | None