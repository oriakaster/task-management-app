import React, { useEffect, useState } from "react";
import { useAuth } from "../auth";
import { api } from "../api";
import TaskForm from "../components/TaskForm";
import TaskItem from "../components/TaskItem";

export default function TasksPage() {
  const { token } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

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
    const t = await api.addTask(token, description);
    setTasks((prev) => [t, ...prev]);
  };

  const toggleTask = async (id, completed) => {
    const t = await api.updateTask(token, id, { completed });
    setTasks((prev) => prev.map((x) => (x.id === id ? t : x)));
  };

  const editTask = async (id, description) => {
    const t = await api.updateTask(token, id, { description });
    setTasks((prev) => prev.map((x) => (x.id === id ? t : x)));
  };

  const deleteTask = async (id) => {
    await api.deleteTask(token, id);
    setTasks((prev) => prev.filter((x) => x.id !== id));
  };

  return (
    <div className="container">
      <TaskForm onAdd={addTask} />
      {err && <div className="error">{err}</div>}
      {loading ? (
        <div className="muted">Loading…</div>
      ) : tasks.length === 0 ? (
        <div className="muted">No tasks yet. Add one above.</div>
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
