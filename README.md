# Task Management App 

## Overview
A simple, secure REST API that lets users register, log in, and manage their personal to-do tasks. Each user can create tasks, list their own tasks, update them (e.g., mark completed), and delete them. Authentication uses JWT Bearer tokens.

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

## Running The Tests
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
pytest -q .\app\tests\test_ver.py
```
---

## Errors (uniform shape)
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



