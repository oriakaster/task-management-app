import React, { useState } from "react";

/** * TaskForm component for adding new tasks.
 * It contains an input field for the task description and a button to submit the task.
  * * @param {Object} props - The properties passed to the component.
 * @param {Function} props.onAdd - Callback function to handle adding a new task.
 * * @returns {JSX.Element} The rendered TaskForm component.
 */
export default function TaskForm({ onAdd }) {
  const [desc, setDesc] = useState("");

  const submit = (e) => {
    e.preventDefault();
    const d = desc.trim();
    if (!d) return;
    onAdd(d);
    setDesc("");
  };

  return (
    <form className="card row" onSubmit={submit}>
      <input
        className="input"
        placeholder="Add a task…"
        value={desc}
        onChange={(e) => setDesc(e.target.value)}
      />
      <button className="btn">Add</button>
    </form>
  );
}
