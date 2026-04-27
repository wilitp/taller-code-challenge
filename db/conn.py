from databases import Database


def get_db():
    db = Database("postgresql+asyncpg://postgres:example@localhost:5432/postgres")
    return db

async def initize_db(db: Database):
    # connect to the database
    await db.connect()
    return db

async def close_db(db: Database):
    # close the database connection
    await db.disconnect()