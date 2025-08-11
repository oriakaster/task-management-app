import React, { createContext, useContext, useMemo, useState } from "react";
import { api } from "./api";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username"));

  const login = async (u, p) => {
    const res = await api.login(u, p); // { access_token }
    setToken(res.access_token);
    setUsername(u);
    localStorage.setItem("token", res.access_token);
    localStorage.setItem("username", u);
  };

  const register = async (u, p) => {
    await api.register(u, p); // returns { id, username }
  };

  const logout = () => {
    setToken(null);
    setUsername(null);
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  };

  const value = useMemo(
    () => ({ token, username, isAuthed: !!token, login, register, logout }),
    [token, username]
  );

  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthCtx);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
