# Task Management App — FastAPI + React

A full‑stack task manager with a FastAPI backend (JWT auth) and a React (Vite) frontend.  
Clean error handling (middleware), clear API schemas, and simple local setup.

---

## ✨ Features
- **Auth**: Register & login with JWT (Bearer token)
- **Tasks**: Create, list, update (partial), delete – scoped per user
- **Consistent errors**: Unified JSON `{ "error": { "code", "message", "fields?" } }`
- **Typed I/O**: Pydantic schemas for inputs/outputs
- **Front‑end**: Minimal React UI you can easily restyle

---

## 🗂️ Project structure (top‑level)
```
Task_Management_App_Assignment/
├─ app/                  # Backend (FastAPI)
│  ├─ app.py             # FastAPI app, includes routers & middleware
│  ├─ core/
│  │  ├─ settings.py     # Loads config from app/.env
│  │  └─ errors.py       # AppError + specific error classes
│  ├─ middleware/
│  │  └─ error_handler.py # Global error middleware (uniform JSON)
│  ├─ data/              # Models, repositories (users, tasks)
│  ├─ database.py        # SQLAlchemy engine/session + get_db dep
│  └─ ...                # routers/services (users, tasks, auth)
├─ frontend/             # Frontend (React + Vite)
│  ├─ src/
│  │  ├─ api.js          # HTTP helper (uses VITE_API_URL)
│  │  ├─ auth.jsx        # Auth context (stores token/username)
│  │  ├─ pages/          # AuthPage.jsx, TasksPage.jsx
│  │  └─ components/     # Navbar, TaskForm, TaskItem, etc.
│  └─ ...                # index.html, vite config, CSS
└─ ...
```

> Names may vary slightly in your repo; commands below match what you’re running now.

---

## ✅ Prerequisites
- **Python 3.11+**
- **Node 18+** and **npm** (or pnpm/yarn)
- **VS Code** (optional, recommended)
- **SQLite** (bundled with Python – no extra install)

---

## ⚙️ Configuration (env files)

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

### Frontend — `frontend/.env.production` (build)
```
VITE_API_URL=https://api.your-domain.com
```

> Don’t commit real secrets. Commit `app/.env.example` and `frontend/.env.example` instead.

---

## ▶️ Running locally (two terminals)

### 1) Backend (FastAPI)
```powershell
# from the project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -U pip
pip install "uvicorn[standard]" fastapi pydantic pydantic-settings sqlalchemy python-jose passlib[bcrypt]

# run the API
uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```
Open Swagger: http://127.0.0.1:8000/docs

### 2) Frontend (Vite)
```powershell
cd frontend
npm install
npm run dev
```
Open the app: the console will print a URL (usually http://127.0.0.1:5173).

---

## 🧪 Tests
If your repo includes pytest tests (e.g., `app/tests/test_edges.py`):

```powershell
# in a new terminal, with backend still running
.\.venv\Scripts\Activate.ps1

pip install pytest httpx
pytest -q
```

There’s also a convenience test you can use to verify the required endpoints quickly. If needed, set `BASE_URL` for tests:
```powershell
$env:BASE_URL="http://127.0.0.1:8000"
pytest -q
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
- `DATABASE_ERROR` / `INTERNAL_SERVER_ERROR` (500) — server error (often includes `errorId`)

---

## 🧠 How things fit together

- **Schemas (Pydantic)**  
  - *Request models*: `UserCreate`, `LoginRequest`, `TaskCreate`, `TaskUpdate`  
  - *Response models*: `UserOut`, `TaskOut`, `Token`  
  They validate incoming data and shape outbound data (and power Swagger).

- **Auth flow**  
  `POST /login` returns `access_token`. Frontend stores it (context + localStorage) and sends it as `Authorization: Bearer ...`.

- **Error middleware**  
  `app/middleware/error_handler.py` intercepts exceptions and produces the consistent JSON shape above (plus field maps for 422). It also normalizes plain 404/405 responses.

- **DB**  
  Default is SQLite (`DATABASE_URL=sqlite:///./app.db`). For other DBs set `DATABASE_URL` (e.g., Postgres) and the app will use it automatically.

---

## 🧩 Environment tips

- If you see **`SECRET_KEY Field required`** on startup, add `SECRET_KEY` to `app/.env` (or give it a default in `settings.py`).
- Change `CORS_ORIGINS` to match your frontend origin (dev is usually `http://127.0.0.1:5173`).
- In the frontend, Vite reads `VITE_*` vars; restart `npm run dev` after changing `.env`.

---

## 🗄️ Viewing the database
Using SQLite? Install VS Code extension **“SQLite” (alexcvzz)**, then open `app.db` and browse tables (`users`, `tasks`).  
Or use SQLTools with the SQLite driver.

---

## 🚀 Production notes (quick)
- Build frontend: `cd frontend && npm run build` (serves static files from `dist/`)
- Configure **`.env.production`** in frontend to point at your real API URL
- Put a reverse proxy (Nginx/Traefik) in front of FastAPI and frontend
- Consider Postgres for production (`DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db`)

---

## 🤝 Troubleshooting

- **Browser says “CORS blocked”**  
  Ensure your frontend origin is listed in `CORS_ORIGINS` (comma‑separated) and restart the backend.

- **Frontend can’t reach API**  
  Check `VITE_API_URL` in `frontend/.env`, and confirm the backend logs show it’s listening on the right host/port.

- **`sqlite3.ProgrammingError: SQLite objects created in a thread…`**  
  The app configures SQLite with `check_same_thread=False` automatically; ensure you run from project root so the DB path is correct.

- **404/405 “Not found” or “Method not allowed”**  
  The middleware rewrites these to your error shape (unless requested as HTML). Double‑check the route and HTTP verb.

---

## 📜 License
For coursework/demo use; adapt as needed.

---

## 🙋 Need help?
Open an issue or ping me with your exact error (logs + request) and I’ll point you to the fix.

