import httpx
import pytest
import random
import string

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="module")
def client():
    with httpx.Client(timeout=10.0) as c:
        yield c

def rnd_user(prefix="u"):
    s = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{prefix}_{s}"

def register(c: httpx.Client, username: str, password: str):
    return c.post(f"{BASE_URL}/register", json={"username": username, "password": password})

def login(c: httpx.Client, username: str, password: str):
    return c.post(f"{BASE_URL}/login", json={"username": username, "password": password})

def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

# ---------- Registration edge cases ----------

def test_register_idempotent_same_password_returns_200(client):
    username = rnd_user("idem")
    pw = "Secret123"
    r1 = register(client, username, pw)
    assert r1.status_code == 200
    uid1 = r1.json()["id"]

    # second registration with same password should succeed (idempotent)
    r2 = register(client, username, pw)
    assert r2.status_code == 200
    uid2 = r2.json()["id"]
    # should be the same user id
    assert uid1 == uid2

def test_register_conflict_when_same_username_different_password(client):
    username = rnd_user("dupe")
    pw1, pw2 = "Secret123", "Different123"

    assert register(client, username, pw1).status_code == 200
    r = register(client, username, pw2)
    # Global handler should map to 409 and structured error
    assert r.status_code == 409
    body = r.json()
    assert body.get("error", {}).get("code") == "USERNAME_TAKEN"

def test_register_validation_422(client):
    # too-short username/password -> Pydantic validation error
    r = client.post(f"{BASE_URL}/register", json={"username": "ab", "password": "x"})
    assert r.status_code == 422

# ---------- Authentication edge cases ----------

def test_login_wrong_password_401_with_code(client):
    username = rnd_user("login")
    pw = "Secret123"
    assert register(client, username, pw).status_code == 200

    r = login(client, username, "WRONGPASS")
    assert r.status_code == 401
    # our global handler (InvalidCredentialsError) should set this code
    assert r.json().get("error", {}).get("code") == "INVALID_CREDENTIALS"

def test_tasks_requires_auth_header_401(client):
    r = client.get(f"{BASE_URL}/tasks")
    assert r.status_code == 401  # produced by OAuth2 (not our handler)

def test_login_with_garbage_token_401(client):
    # Use a completely invalid JWT
    headers = {"Authorization": "Bearer not_a_real_token"}
    r = client.get(f"{BASE_URL}/tasks", headers=headers)
    assert r.status_code == 401

# ---------- Tasks edge cases ----------

def test_task_crud_and_cross_user_forbidden(client):
    # user A
    user_a, pw_a = rnd_user("a"), "Secret123"
    assert register(client, user_a, pw_a).status_code == 200
    tok_a = login(client, user_a, pw_a).json()["access_token"]
    ha = auth_headers(tok_a)

    # user B
    user_b, pw_b = rnd_user("b"), "Secret123"
    assert register(client, user_b, pw_b).status_code == 200
    tok_b = login(client, user_b, pw_b).json()["access_token"]
    hb = auth_headers(tok_b)

    # A creates a task
    r_create = client.post(f"{BASE_URL}/tasks", headers=ha, json={"description": "A's secret task"})
    assert r_create.status_code == 200
    task_id = r_create.json()["id"]

    # B tries to read/update/delete A's task -> 403 with TASK_FORBIDDEN
    r_read = client.put(f"{BASE_URL}/tasks/{task_id}", headers=hb, json={"completed": True})
    assert r_read.status_code == 403
    assert r_read.json().get("error", {}).get("code") == "TASK_FORBIDDEN"

    r_del = client.delete(f"{BASE_URL}/tasks/{task_id}", headers=hb)
    assert r_del.status_code == 403
    assert r_del.json().get("error", {}).get("code") == "TASK_FORBIDDEN"

def test_update_nonexistent_task_404(client):
    user, pw = rnd_user("missing"), "Secret123"
    assert register(client, user, pw).status_code == 200
    token = login(client, user, pw).json()["access_token"]
    headers = auth_headers(token)

    r = client.put(f"{BASE_URL}/tasks/99999999", headers=headers, json={"completed": True})
    assert r.status_code == 404
    assert r.json().get("error", {}).get("code") == "TASK_NOT_FOUND"

def test_partial_update_only_completed_field(client):
    user, pw = rnd_user("partial"), "Secret123"
    assert register(client, user, pw).status_code == 200
    token = login(client, user, pw).json()["access_token"]
    headers = auth_headers(token)

    # create
    r_create = client.post(f"{BASE_URL}/tasks", headers=headers, json={"description": "Buy milk"})
    assert r_create.status_code == 200
    tid = r_create.json()["id"]

    # partial update: only 'completed'
    r_upd = client.put(f"{BASE_URL}/tasks/{tid}", headers=headers, json={"completed": True})
    assert r_upd.status_code == 200
    body = r_upd.json()
    assert body["completed"] is True
    assert body["description"] == "Buy milk"  # unchanged

def test_delete_idempotent_behavior(client):
    user, pw = rnd_user("del"), "Secret123"
    assert register(client, user, pw).status_code == 200
    token = login(client, user, pw).json()["access_token"]
    headers = auth_headers(token)

    # create then delete
    tid = client.post(f"{BASE_URL}/tasks", headers=headers, json={"description": "to delete"}).json()["id"]
    r1 = client.delete(f"{BASE_URL}/tasks/{tid}", headers=headers)
    assert r1.status_code == 200

    # deleting again should return 404 TASK_NOT_FOUND (not 200)
    r2 = client.delete(f"{BASE_URL}/tasks/{tid}", headers=headers)
    assert r2.status_code == 404
    assert r2.json().get("error", {}).get("code") == "TASK_NOT_FOUND"
