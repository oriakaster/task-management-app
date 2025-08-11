# app/app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import re
from .database import Base, engine
from .data import models  # ensure models are imported so tables register
from .routers import users, tasks
from .core.errors import AppError
import json
from app.middleware.error_handler import ErrorHandlingMiddleware

# (optional) if you set up minimal logging in app/core/logging.py, enable it:
try:
    from .core.logging import setup_logging
except ModuleNotFoundError:
    pass
else:
    setup_logging()

app = FastAPI(title="Task Management API")
app.add_middleware(ErrorHandlingMiddleware)
# @app.exception_handler(AppError)
# async def handle_app_error(request: Request, exc: AppError):
#     """input: AppError with code, message, http_status
#        output: JSON response with error details
#        uniform error handling for domain errors"""
#     payload = {"error": {"code": exc.code, "message": exc.message}}
#     print(json.dumps(payload, ensure_ascii=False, indent=2))
#     return JSONResponse(status_code=exc.http_status, content=payload)

@app.middleware("http")
async def collapse_slashes(request: Request, call_next):
  """input: Request with path like /register or //register
     output: Request with normalized path like /register
     middleware to ensure no double slashes in paths"""
  path = request.scope.get("path", "")
  if "//" in path:
    request.scope["path"] = re.sub(r"/{2,}", "/", path)
  return await call_next(request)

# ---- CORS (prep for a local frontend on 3000/5173, etc.) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:5173", "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Create DB tables (after models import) ----
Base.metadata.create_all(bind=engine)

# ---- Routers ----
app.include_router(users.router)   # /register, /login
app.include_router(tasks.router)   # /tasks, /tasks/{id}

@app.get("/", response_class=HTMLResponse)
def index():
    """input: GET /
       output: HTML landing page with API info
       simple HTML response to show API is running"""
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Task Management API</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 40px; }
    .card { max-width: 720px; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; }
    h1 { margin: 0 0 12px; font-size: 24px; }
    code { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
    a { color: #2563eb; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .row { margin-top: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <h1> Task Management API is running</h1>
    <div class="row">Interactive docs: <a href="/docs">/docs</a></div>
    <div class="row" style="margin-top:18px;">
      <strong>Quick start:</strong>
      <ol>
        <li><code>POST /register</code> with <code>{"username":"u","password":"p"}</code></li>
        <li><code>POST /login</code> ⇒ copy <em>access_token</em></li>
        <li>Click <em>Authorize</em> in /docs: <code>Bearer &lt;token&gt;</code></li>
        <li>Use <code>/tasks</code> endpoints</li>
      </ol>
    </div>
    <div class="row">
      <strong>Frontend prep:</strong> CORS enabled for <code>localhost:3000</code> and <code>5173</code>.
    </div>
  </div>
</body>
</html>
    """
