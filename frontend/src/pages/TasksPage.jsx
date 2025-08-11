import React, { useEffect, useState } from "react";
import { useAuth } from "../auth";
import { api } from "../api";
import TaskForm from "../components/TaskForm";
import TaskItem from "../components/TaskItem";

/** * TasksPage component for managing user tasks.
 * It allows users to view, add, edit, toggle completion status, and delete tasks.
 * * @returns {JSX.Element} The rendered TasksPage component.
 */
export default function TasksPage() {
  const { token } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  // Map backend error codes -> friendly messages for the UI
  const mapTaskError = (e) => {
    if (!e) return "Something went wrong";
    if (e.code === "TASK_NOT_FOUND")   return "That task was deleted or doesn't exist.";
    if (e.code === "TASK_FORBIDDEN")   return "You don't have access to this task.";
    if (e.code === "DATABASE_ERROR")   return "Database error. Please try again.";
    if (e.code === "INTERNAL_SERVER_ERROR") return "Unexpected error. Try again.";
    return e.message || "Something went wrong";
  };

  const load = async () => {
    setErr("");
    try {
      setLoading(true);
      const items = await api.listTasks(token);
      setTasks(items);
    } catch (ex) {
      setErr(ex.message || "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, []);

  const addTask = async (description) => {
    setErr("");
    try {
      const t = await api.addTask(token, description);
      setTasks((prev) => [t, ...prev]); 
    } catch (e) {
      setErr(mapTaskError(e));
    }
  };

  const toggleTask = async (id, completed) => {
    setErr("");
    try {
      const t = await api.updateTask(token, id, { completed });
      setTasks((prev) => prev.map((x) => (x.id === id ? t : x)));
    } catch (e) {
      setErr(mapTaskError(e));
    }
  };

  const editTask = async (id, description) => {
    setErr("");
    try {
      const t = await api.updateTask(token, id, { description });
      setTasks((prev) => prev.map((x) => (x.id === id ? t : x)));
    } catch (e) {
      setErr(mapTaskError(e));
    }
  };

  const deleteTask = async (id) => {
    setErr("");
    try {
      await api.deleteTask(token, id);
      setTasks((prev) => prev.filter((x) => x.id !== id));
    } catch (e) {
      setErr(mapTaskError(e));
    }
  };

  return (
    <div className="container">
      <div className="titlebar">
        <h1 className="h1">My Tasks</h1>
        <div className="kpis">
          <span className="kpi">Total: {tasks.length}</span>
          <span className="kpi">Done: {tasks.filter(t=>t.completed).length}</span>
        </div>
      </div>

      <TaskForm onAdd={addTask} />
      {err && <div className="error">{err}</div>}

      {loading ? (
        <div className="placeholder"><span className="spinner" />Loading your tasks…</div>
      ) : tasks.length === 0 ? (
        <div className="placeholder">No tasks yet. Add your first task above ✨</div>
      ) : (
        <div className="col gap">
          {tasks.map((t) => (
            <TaskItem
              key={t.id}
              task={t}
              onToggle={toggleTask}
              onEdit={editTask}
              onDelete={deleteTask}
            />
          ))}
        </div>
      )}
    </div>
  );
}
