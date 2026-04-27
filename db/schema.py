import asyncio
from databases import Database
from conn import get_db, initize_db, close_db


schema_statements = [
"""
CREATE TABLE Project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",

"""CREATE TABLE Task (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES Project(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    priority INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    due_date DATE
);""",
"""
-- create index on (project_id, priority), descending on the priority key
CREATE INDEX idx_task_project_priority ON Task (project_id, priority DESC);
"""
]

async def create_schema():
    db = get_db()
    await initize_db(db)
    async with db.transaction():
        for statement in schema_statements:
            await db.execute(statement)
    await close_db(db)

if __name__ == "__main__":
    asyncio.run(create_schema())