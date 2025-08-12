# Task Management App — FastAPI + React

A full‑stack task manager with a FastAPI backend (JWT auth) and a React (Vite) frontend.  
Clean error handling (middleware), clear API schemas, and simple local setup.

---

## Features
- **Auth**: Register & login with JWT (Bearer token)
- **Tasks**: Create, list, update (partial), delete – scoped per user
- **Consistent errors**: Unified JSON `{ "error": { "code", "message", "fields?" } }`
- **Typed I/O**: Pydantic schemas for inputs/outputs
- **Front‑end**: Minimal React UI

---

## Tech Stack
**Backend:** FastAPI, SQLAlchemy, Uvicorn  
**Frontend:** React 18, Vite, React Router  
**Database:** SQLite by default (swap to Postgres/MySQL if desired)

---

## Prerequisites
- **Python 3.11+**
- **Node 18+** and **npm** (or pnpm/yarn)
- **VS Code** (optional, recommended)
- **SQLite** (bundled with Python – no extra install)

Check versions:
```bash
python --version
node --version
npm --version
```

---

## Environment Variables

### Backend — `app/.env`
Create a file `app/.env`:
```
APP_ENV=dev
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=change-me                # use a strong random string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

> Tip (Windows PowerShell): generate a strong secret
> ```powershell
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

### Frontend — `frontend/.env` (dev)
Create `frontend/.env`:
```
VITE_API_URL=http://127.0.0.1:8000
```

> Don’t commit real secrets. Commit `app/.env.example` and `frontend/.env.example` instead.

---

## Running locally (two terminals)

## Backend Setup (FastAPI)

1) **Create and activate a virtual environment**

**Windows (PowerShell):**
```powershell
# from the project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux (bash/zsh):**
```bash
python -m venv .venv
source .venv/bin/activate
```

2) **Install dependencies**
```powershell
pip install -r requirements.txt
```

3) **Configure environment**
Create `app/.env` (see [Environment Variables](#environment-variables)).

4) **Run the server**
```powershell
uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```
Your API will be available at http://127.0.0.1:8000/docs 
Use this to explore endpoints and try requests interactively.

---
## Frontend Setup (React + Vite)

in a new terminal:

1) **Install dependencies**
```powershell
# in a new terminal
.\.venv\Scripts\Activate.ps1
cd frontend
npm install
```

2) **Configure environment**
Create `frontend/.env` (see [Environment Variables](#environment-variables)).

3) **Run the dev server**
```powershell
npm run dev
```
Open the app: the console will print a URL (usually http://127.0.0.1:5173 or http://localhost:5173/).
Vite will print the exact URL in the terminal.

---

## Tests
If you want to run the tests:

```powershell
# in a new terminal, with backend still running
.\.venv\Scripts\Activate.ps1

pip install pytest httpx
pytest -q
```

you can also run specific test file, for example:

```
pip install pytest httpx
pytest -q app/tests/test_ver.py
```
---

## 🔌 API summary (contract)

### Auth
- `POST /register` — create user  
  **Request** `{"username": "...", "password": "..."}`  
  **Response** `{"id": 1, "username": "..."}`

- `POST /login` — get JWT  
  **Request** `{"username": "...", "password": "..."}`  
  **Response** `{"access_token": "...", "token_type": "bearer"}`

> Send the token on subsequent requests: `Authorization: Bearer <token>`

### Tasks
- `GET /tasks` — list my tasks → **200** `[{ TaskOut }]`
- `POST /tasks` — create task → **200** `{ TaskOut }`  
  body: `{"description":"..."}`
- `PUT /tasks/{id}` — partial update → **200** `{ TaskOut }`  
  body: `{"description":"..."}` or `{"completed": true}`
- `DELETE /tasks/{id}` — delete → **200** `{ "message": "deleted" }` (shape may vary)

### Errors (uniform shape)
All failures come back as JSON:
```json
{ "error": { "code": "SOME_CODE", "message": "Human readable", "fields": { "field": ["msg"] } } }
```
Common codes:
- `INVALID_TOKEN` (401) — missing/invalid/expired JWT
- `USERNAME_TAKEN` (409) — registering an existing username
- `USER_NOT_FOUND` (404) — login with unknown username
- `INVALID_PASSWORD` (401) — login with wrong password
- `TASK_NOT_FOUND` (404) — updating/deleting a missing task
- `TASK_FORBIDDEN` (403) — touching someone else’s task
- `VALIDATION_ERROR` (422) — input validation failed
- `DATABASE_ERROR` / `INTERNAL_SERVER_ERROR` (500) — server error

---

##  Short Explanation
- **What it is:** A full-stack Task Manager.
Backend: FastAPI + SQLAlchemy + Pydantic (JWT auth).
Frontend: React (Vite) SPA.

- **What it does:** Users can register and log in, then create, list, update, and delete their own tasks. Each task has description and completed.

- **Security:** After login, the frontend stores a JWT. Every tasks request sends Authorization: Bearer <token>. The backend validates the token and scopes actions to the current user (can’t touch others’ tasks).

- **API endpoints:** POST /register, POST /login, GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE { "message": "Task deleted successfully" }.

- **Validation & schemas:** Pydantic models validate request bodies (UserCreate, TaskCreate, TaskUpdate) and shape responses (UserOut, TaskOut, Token).

- **Data & startup:** Uses SQLite by default (app.db). Tables are created on startup if missing.

- **Frontend flow:** AuthPage handles login/register, TasksPage shows and edits tasks. api.js attaches the JWT automatically and normalizes error responses for friendly messages.

---

## Troubleshooting

- **Browser says “CORS blocked”**  
  Ensure your frontend origin is listed in `CORS_ORIGINS` (comma‑separated) and restart the backend.

- **Frontend can’t reach API**  
  Check `VITE_API_URL` in `frontend/.env`, and confirm the backend logs show it’s listening on the right host/port.

- **`sqlite3.ProgrammingError: SQLite objects created in a thread…`**  
  The app configures SQLite with `check_same_thread=False` automatically; ensure you run from project root so the DB path is correct.

- **404/405 “Not found” or “Method not allowed”**  
  The middleware rewrites these to your error shape (unless requested as HTML). Double‑check the route and HTTP verb.


