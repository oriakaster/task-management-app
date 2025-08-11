// Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth";

export default function Navbar() {
  const { isAuthed, username, logout } = useAuth();
  return (
    <nav className="nav">
      <div className="nav-left">
        <Link to="/" className="brand"> Task Manager</Link>
        {isAuthed && <Link to="/tasks" className="nav-link">My Tasks</Link>}
      </div>
      <div className="nav-right">
        {isAuthed ? (
          <>
            <span className="muted">Hi, {username}</span>
            <button className="btn ghost" onClick={logout}>Logout</button>
          </>
        ) : (
          <Link to="/login" className="btn">Login</Link>
        )}
      </div>
    </nav>
  );
}
