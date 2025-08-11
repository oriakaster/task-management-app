import React, { useState } from "react";
import { useAuth } from "../auth";
import { useNavigate } from "react-router-dom";

/** * AuthPage component for user authentication (login/register).
 * It allows users to log in or register a new account.
 * * @returns {JSX.Element} The rendered AuthPage component.
 */
export default function AuthPage() {
  const nav = useNavigate();
  const { login, register } = useAuth();
  const [mode, setMode] = useState("login"); // or "register"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

    // Map backend error codes -> messages shown in the UI
  const mapAuthError = (ex) => {
    if (ex?.code === "USER_NOT_FOUND")   return "Username does not exist, please register";
    if (ex?.code === "INVALID_PASSWORD") return "Password is incorrect, please try again";
    if (ex?.code === "USERNAME_TAKEN")   return "That username is already taken, please choose another";
    if (ex?.status === 401)              return "Invalid username or password";
    return ex?.message || "Something went wrong";
  };

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
      setErr(mapAuthError(ex));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container narrow">
      <div className="titlebar">
        <h1 className="h1">{mode === "login" ? "Welcome back" : "Create your account"}</h1>
        <div className="kpis">
          <span className="kpi">{mode === "login" ? "Sign in" : "Join now"}</span>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${mode === "login" ? "active" : ""}`} onClick={() => setMode("login")}>Login</button>
        <button className={`tab ${mode === "register" ? "active" : ""}`} onClick={() => setMode("register")}>Register</button>
      </div>

      <form className="card col" onSubmit={submit}>
        <input className="input" placeholder="Username" value={username} minLength={3} onChange={(e)=>setUsername(e.target.value)} required />
        <input className="input" placeholder="Password" value={password} minLength={4} onChange={(e)=>setPassword(e.target.value)} type="password" required />
        {err && <div className="error">{err}</div>}
        <button className="btn" disabled={busy}>
          {busy ? "Please wait…" : (mode === "login" ? "Login" : "Create account")}
        </button>
      </form>
    </div>
  );
}