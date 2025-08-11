# Task Management App — FastAPI + React (Vite)

A simple task manager with a FastAPI backend and a React (Vite) frontend.

---

## Table of Contents
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup (FastAPI)](#backend-setup-fastapi)
- [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
- [Run the App](#run-the-app)
- [Environment Variables](#environment-variables)
- [API Docs](#api-docs)
- [Troubleshooting](#troubleshooting)
- [Useful Scripts](#useful-scripts)
- [Production Notes](#production-notes)

---

## Tech Stack
**Backend:** FastAPI, SQLAlchemy, Uvicorn  
**Frontend:** React 18, Vite, React Router  
**Database:** SQLite by default (swap to Postgres/MySQL if desired)

---

## Prerequisites
- **Python** ≥ 3.10 (recommended)
- **Node.js** ≥ 18 and **npm**
- **Git** (optional but recommended)

Check versions:
```bash
python --version
node --version
npm --version
```

---

## Project Structure
```
.
├── backend/
│   ├── app/                    # FastAPI code (routers, models, crud, etc.)
│   ├── requirements.txt
│   └── .env                    # Backend config (see below)
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts|js
│   └── .env                    # Frontend config (see below)
└── README.md
```
> If your folders are named differently, adjust paths accordingly.

---

## Backend Setup (FastAPI)

1) **Create and activate a virtual environment**

**Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux (bash/zsh):**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

2) **Install dependencies**
```bash
pip install -r requirements.txt
```

3) **Configure environment**
Create `backend/.env` (see [Environment Variables](#environment-variables)).

4) **Initialize the database**
If your app creates tables on startup, you can skip. Otherwise, run your migrations (if you use Alembic):
```bash
# Example only—use if Alembic is configured
alembic upgrade head
```

5) **Run the server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Your API will be available at http://localhost:8000

---

## Frontend Setup (React + Vite)

1) **Install dependencies**
```bash
cd frontend
npm install
```

2) **Configure environment**
Create `frontend/.env` (see [Environment Variables](#environment-variables)).

3) **Run the dev server**
```bash
npm run dev
```
Vite will print a local URL, typically http://localhost:5173

---

## Run the App

- Start **backend** (port **8000**):
  ```bash
  # from backend/
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- Start **frontend** (port **5173**):
  ```bash
  # from frontend/
  npm run dev
  ```

- Open the UI in your browser:
  ```
  http://localhost:5173
  ```

- The frontend calls the backend at:
  ```
  http://localhost:8000
  ```
  (configurable via env vars below)

---

## Environment Variables

### Backend (`backend/.env`)
```env
# Environment
APP_ENV=dev

# Database (SQLite by default)
DATABASE_URL=sqlite:///./app.db
# Example Postgres:
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/mydb

# CORS (frontend origin)
CORS_ORIGINS=http://localhost:5173

# Auth (if your app uses JWT)
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Make sure your FastAPI app loads these (e.g., with `pydantic-settings` or `python-dotenv`).

### Frontend (`frontend/.env`)
```env
# Where the frontend sends API calls
VITE_API_BASE_URL=http://localhost:8000
```
In React code: `import.meta.env.VITE_API_BASE_URL`

---

## API Docs
FastAPI auto-generates docs:
- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI JSON:** http://localhost:8000/openapi.json

Use this to explore endpoints and try requests interactively.

---

## Troubleshooting

**Duplicate `node_modules` / multiple frontend folders**
- Ensure you only have **one** frontend project folder (e.g., `frontend/`).
- If you accidentally created two (e.g., `task-ui/` and `frontend/`), keep one and delete the other.
- After cleaning, reinstall:
  ```bash
  cd frontend
  # macOS/Linux
  rm -rf node_modules package-lock.json
  npm install
  # Windows (PowerShell)
  rmdir /s /q node_modules
  del /f /q package-lock.json
  npm install
  ```

**CORS errors in the browser**
- Add your frontend origin (e.g., `http://localhost:5173`) to `CORS_ORIGINS` in `backend/.env`.
- Ensure FastAPI enables CORS:
  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=[origins_from_env],  # e.g., ["http://localhost:5173"]
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

**Port already in use**
- Backend 8000: stop the other process or change `--port`.
- Frontend 5173: Vite usually picks another port automatically, or `npm run dev -- --port 5174`.

**Virtual environment not activating (Windows)**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Database not created / permission issues**
- If using SQLite, ensure `DATABASE_URL=sqlite:///./app.db` and that the process has write permission to the folder.
- For Postgres/MySQL, verify the connection string and that the database exists.

---

## Useful Scripts

**Backend**
```bash
# from backend/
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
# from frontend/
npm install
npm run dev
npm run build         # build for production
npm run preview       # preview the production build
```

---

## Production Notes
- Build the frontend and serve the static files via a web server (e.g., Nginx) or from FastAPI if you prefer.
- Run FastAPI behind a process manager with multiple workers (e.g., `gunicorn -k uvicorn.workers.UvicornWorker -w 2`).
- Use a managed database for durability and backups instead of SQLite.
- Configure HTTPS and a reverse proxy for security and performance.
