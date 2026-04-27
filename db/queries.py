from databases import Database
from datetime import datetime


async def create_project(database: Database, name: str, description: str):
    query = """
    INSERT INTO Project (name, description) VALUES (:name, :description) RETURNING id
    """
    return await database.execute(query, {"name": name, "description": description})

async def read_project(database: Database, project_id: int):
    query = """
    SELECT * FROM Project WHERE id = :project_id
    """
    return await database.fetch_one(query, {"project_id": project_id})

async def update_project(database: Database, project_id: int, name, description):
    query = """
    UPDATE Project 
    SET 
    name = COALESCE(:name, name), 
    description = COALESCE(:description, description) 
    WHERE id = :project_id
    RETURNING id
    """
    return await database.execute(query, {"project_id": project_id, "name": name, "description": description})

async def delete_project(database: Database, project_id: int) -> bool:
    query = """
    DELETE FROM Project WHERE id = :project_id RETURNING id
    """
    # delete project with id project_id, return true if a row was deleted, false otherwise
    return await database.execute(query, {"project_id": project_id})

async def create_task(database: Database, project_id: int, title: str, priority: int, completed: bool = False, due_date: datetime | None = None):
    query = """
    INSERT INTO Task (project_id, title, priority, completed, due_date) 
    VALUES (:project_id, :title, :priority, :completed, :due_date) RETURNING id
    """

    try:
        return await database.execute(query, {
            "project_id": project_id,
            "title": title,
            "priority": priority,
            "completed": completed,
            "due_date": due_date
        })
    except Exception as e:
        return None;

async def read_tasks(database: Database, project_id: int):
    query = """
    SELECT * FROM Task WHERE project_id = :project_id ORDER BY priority DESC
    """
    return await database.fetch_all(query, {"project_id": project_id})

async def update_task(database: Database, task_id: int, title=None, priority=None, completed=None, due_date=None):
    query = """
    UPDATE Task SET 
        title = COALESCE(:title, title), 
        priority = COALESCE(:priority, priority), 
        completed = COALESCE(:completed, completed), 
        due_date = COALESCE(:due_date, due_date) 
    WHERE id = :task_id
    RETURNING id
    """
    return await database.execute(query, {
        "task_id": task_id,
        "title": title,
        "priority": priority,
        "completed": completed,
        "due_date": due_date
    })

async def delete_task(database: Database, task_id: int):
    query = """
    DELETE FROM Task WHERE id = :task_id RETURNING id
    """
    return await database.execute(query, {"task_id": task_id})