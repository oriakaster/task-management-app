# app/main.py
import re
from fastapi import FastAPI, Request

from .database import Base, engine          # DB engine + metadata
from .data import models                    # import models so tables are registered
from .routers import users, tasks           # presentation layer (endpoints)

app = FastAPI(title="Task Management API")

# ---- Normalize paths like //register -> /register (keeps tests happy) ----
@app.middleware("http")
async def collapse_slashes(request: Request, call_next):
    path = request.scope.get("path", "")
    if "//" in path:
        request.scope["path"] = re.sub(r"/{2,}", "/", path)
    return await call_next(request)

# ---- Create tables (after models are imported) ----
Base.metadata.create_all(bind=engine)

# ---- Register routers ----
app.include_router(users.router)   # /register, /login
app.include_router(tasks.router)   # /tasks, /tasks/{id}

# ---- Simple health endpoint ----
@app.get("/")
def root():
    return {"message": "Task API is running"}