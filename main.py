from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # get db connection from conn.py
    yield
    # close db connection

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pass


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}