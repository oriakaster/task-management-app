const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/**
 * Makes an API request to the backend.
 * @param {string} path - The API endpoint path.
 * @param {Object} options - The request options.
 * @param {string} [options.method='GET'] - The HTTP method to use.
 * @param {Object} [options.body] - The request body, if applicable.
 * @param {string} [options.token] - The authentication token, if required.
 * @returns {Promise<Object>} The parsed JSON response from the API.
 * @throws {Error} If the request fails or the response is not OK.
 */
async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });


  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!res.ok) {
    const err = new Error(
      data?.error?.message || data?.detail || res.statusText
    );
    err.status = res.status;
    err.code = data?.error?.code;
    throw err;
  }
  return data;
}

export const api = {
  register: (username, password) =>
    request("/register", { method: "POST", body: { username, password } }),

  login: (username, password) =>
    request("/login", { method: "POST", body: { username, password } }),

  listTasks: (token) => request("/tasks", { token }),
  addTask: (token, description) =>
    request("/tasks", { method: "POST", token, body: { description } }),
  updateTask: (token, id, patch) =>
    request(`/tasks/${id}`, { method: "PUT", token, body: patch }),
  deleteTask: (token, id) =>
    request(`/tasks/${id}`, { method: "DELETE", token }),
};
