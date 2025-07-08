// src/App.js
import React from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import AdminPage from "./pages/AdminPage";
import AdminLimitedPage from "./pages/AdminLimitedPage";
import AgentPage from "./pages/AgentPage";
import ViewerPage from "./pages/ViewerPage";

function App() {
  return (
    <Routes>
      {/* Public Route */}
      <Route path="/" element={<LoginPage />} />

      {/* Protected Routes */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<h2>Welcome to the Dashboard</h2>} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/admin-limited" element={<AdminLimitedPage />} />
        <Route path="/agent" element={<AgentPage />} />
        <Route path="/viewer" element={<ViewerPage />} />
      </Route>
    </Routes>
  );
}

export default App;
