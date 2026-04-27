import asyncio
from databases import Database


# data model

"""
Project:

id (UUID or int)

name (string, required)

description (string, optional)

created_at (timestamp)

Task:

id (UUID or int)

project_id (foreign key to Project)

title (string, required)

priority (integer, higher number = higher priority)

completed (boolean, default False)

due_date (date, optional)

"""
schema = """

CREATE TABLE Project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE Task (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES Project(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    priority INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    due_date DATE
)

-- create index on (project_id, priority), descending on the priority key
CREATE INDEX idx_task_project_priority ON Task (project_id, priority DESC);
"""



async def create_schema():
    async with Database("postgresql://postgres:localhost:5432") as database:
        # execute the schema creation SQL commands
        await database.execute(schema)

if __name__ == "__main__":
    asyncio.run(create_schema())