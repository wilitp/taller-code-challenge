from fastapi.exceptions import HTTPException

from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.conn import initize_db, close_db, get_db
from models import CreateTask, Project, Task, UpdateProject
from db.queries import create_project, read_project, update_project, delete_project, create_task, read_tasks, update_task, delete_task
from databases import Database

database: Database = get_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # get db connection from conn.py
    global database
    database = await initize_db(database)
    yield
    # close db connection
    await close_db(database)

app = FastAPI(lifespan=lifespan)


@app.post("/projects/")
async def on_create_project(project: Project):
    return await create_project(database, project.name, project.description)


@app.get("/projects/{project_id}")
async def on_read_project(project_id: int):
    # Implementation for reading a project by ID
    project = await read_project(database, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}")
async def on_update_project(project_id: int, project: UpdateProject):
    # Implementation for updating a project by ID
    project_id = await update_project(database, project_id, project.name, project.description)
    if not project_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_id

@app.delete("/projects/{project_id}")
async def on_delete_project(project_id: int):
    # Implementation for deleting a project by ID
    deleted_id =  await delete_project(database, project_id)

    if not deleted_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}

@app.post("/projects/{project_id}/tasks/")
async def on_create_task(project_id: int, task: CreateTask):
    # Implementation for creating a task within a project
    created_id = await create_task(database, project_id, task.title, task.priority, task.completed, task.due_date)
    if not created_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return created_id

@app.get("/projects/{project_id}/tasks/")
async def on_read_tasks(project_id: int):
    # Implementation for reading tasks within a project
    return await read_tasks(database, project_id)

@app.put("/tasks/{task_id}")
async def on_update_task(project_id: int, task_id: int):
    # Implementation for updating a task within a project
    updated_id = await update_task(database, task_id, project_id)

    if not updated_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_id

@app.delete("/tasks/{task_id}")
async def on_delete_task(project_id: int, task_id: int):
    # Implementation for deleting a task within a project
    deleted_id = await delete_task(database, task_id, project_id)
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}