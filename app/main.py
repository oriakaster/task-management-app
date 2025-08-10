# app/main.py
import re
from fastapi import FastAPI, Request
from .database import Base, engine        
from .data import models                  
from .routers import users, tasks  
from fastapi.responses import JSONResponse
from .core.errors import AppError        

from .core.logging import setup_logging
setup_logging()

app = FastAPI(title="Task Management API")

@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError):
    payload = {"error": {"code": exc.code, "message": exc.message}}
    print(f"[AppError] {request.method} {request.url.path} -> {exc.http_status} {payload}")
    return JSONResponse(status_code=exc.http_status, content=payload)

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