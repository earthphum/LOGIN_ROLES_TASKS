// src/components/ProtectedRoute.js
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();

  if (!localStorage.getItem("access_token")) {
    // เช็ค token ก่อน
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoute;
