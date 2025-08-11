import React, { useState } from "react";

/** * TaskItem component for displaying and managing individual tasks.
 * It allows toggling completion status, editing the task description, and deleting the task.
 * @param {Object} props - The properties passed to the component.
 * @param {Object} props.task - The task object containing id, description, and completion status.
 * @param {Function} props.onToggle - Callback function to handle toggling the task completion status.
 * @param {Function} props.onEdit - Callback function to handle editing the task description.
 * @param {Function} props.onDelete - Callback function to handle deleting the task.
 * * @returns {JSX.Element} The rendered TaskItem component.
 */
export default function TaskItem({ task, onToggle, onEdit, onDelete }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(task.description);

  const save = () => {
    const v = value.trim();
    if (!v || v === task.description) { setEditing(false); return; }
    onEdit(task.id, v);
    setEditing(false);
  };

  return (
    <div className={`card row task ${task.completed ? "done" : ""}`} style={{transition:'transform .06s ease-in-out'}}>
      <label className="checkbox">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => onToggle(task.id, !task.completed)}
        />
        <span />
      </label>

      {editing ? (
        <input
          className="input flex"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && save()}
          autoFocus
        />
      ) : (
        <div className="flex">{task.description}</div>
      )}

      {editing ? (
        <button className="btn secondary" onClick={save}>Save</button>
      ) : (
        <button className="btn secondary" onClick={() => setEditing(true)}>Edit</button>
      )}

      <button className="btn danger" onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
}
