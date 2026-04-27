from pydantic import BaseModel
from datetime import datetime


class Project(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: str | None = None

class UpdateProject(BaseModel):
    name: str | None = None
    description: str | None = None

class Task(BaseModel):
    id: int
    project_id: int
    title: str
    priority: int
    completed: bool = False
    due_date: str | None = None

class CreateTask(BaseModel):
    title: str
    priority: int
    completed: bool = False
    due_date: datetime | None = None