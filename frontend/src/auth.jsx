import React, { createContext, useContext, useMemo, useState } from "react";
import { api } from "./api";

const AuthCtx = createContext(null);

/** * AuthProvider component to manage authentication state.
 * Provides login, register, and logout functionalities.
 * * @param {Object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render within the provider.
 * @returns {JSX.Element} The AuthProvider component. 
 * @throws {Error} If used outside of AuthProvider.
 */
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username"));

  const login = async (u, p) => {
    const res = await api.login(u, p); 
    setToken(res.access_token);
    setUsername(u);
    localStorage.setItem("token", res.access_token);
    localStorage.setItem("username", u);
  };

  const register = async (u, p) => {
    await api.register(u, p); 
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

/**
 * Custom hook to access the authentication context.
 * @returns {Object} The authentication context value.
 * @throws {Error} If used outside of AuthProvider.
 */
export function useAuth() {
  const ctx = useContext(AuthCtx);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
