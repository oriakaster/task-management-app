import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../auth";

export default function ProtectedRoute() {
  const { isAuthed } = useAuth();
  return isAuthed ? <Outlet /> : <Navigate to="/login" replace />;
}
