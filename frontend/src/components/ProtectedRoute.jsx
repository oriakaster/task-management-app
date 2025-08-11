import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../auth";

/** * ProtectedRoute component that checks if the user is authenticated.
 * If authenticated, it renders the children components.
 * If not authenticated, it redirects to the login page.  
 * * @returns {JSX.Element} The rendered ProtectedRoute component.
 */
export default function ProtectedRoute() {
  const { isAuthed } = useAuth();
  return isAuthed ? <Outlet /> : <Navigate to="/login" replace />;
}
