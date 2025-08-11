import React, { useState } from "react";

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
