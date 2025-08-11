import React, { useState } from "react";
import { useAuth } from "../auth";
import { useNavigate } from "react-router-dom";

export default function AuthPage() {
  const nav = useNavigate();
  const { login, register } = useAuth();
  const [mode, setMode] = useState("login"); // or "register"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    try {
      setBusy(true);
      if (mode === "register") {
        await register(username, password);
      }
      await login(username, password);
      nav("/tasks");
    } catch (ex) {
      setErr(ex.message || "Failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container narrow">
      <div className="tabs">
        <button
          className={`tab ${mode === "login" ? "active" : ""}`}
          onClick={() => setMode("login")}
        >Login</button>
        <button
          className={`tab ${mode === "register" ? "active" : ""}`}
          onClick={() => setMode("register")}
        >Register</button>
      </div>

      <form className="card col" onSubmit={submit}>
        <input
          className="input"
          placeholder="Username"
          value={username}
          minLength={3}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          className="input"
          placeholder="Password"
          value={password}
          minLength={4}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          required
        />
        {err && <div className="error">{err}</div>}
        <button className="btn" disabled={busy}>
          {busy ? "Please wait…" : mode === "login" ? "Login" : "Create account"}
        </button>
      </form>
    </div>
  );
}
