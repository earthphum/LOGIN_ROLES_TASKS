// src/components/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Sidebar = () => {
  const { user, logout } = useAuth();

  if (!user) return null; // ถ้ายังไม่มีข้อมูล user ให้ซ่อน sidebar

  const role = user.role;

  return (
    <div
      style={{
        width: "200px",
        borderRight: "1px solid #ccc",
        minHeight: "100vh",
        padding: "1rem",
      }}
    >
      <h3>สวัสดี, {user.username}</h3>
      <p>Role: {role}</p>
      <hr />
      <nav>
        <ul>
          {/* Admin เห็นทุกอย่าง */}
          {role === "ADMIN" && (
            <>
              <li>
                <Link to="/admin">Admin Dashboard</Link>
              </li>
              <li>
                <Link to="/admin-limited">Admin Limited</Link>
              </li>
              <li>
                <Link to="/agent">Agent View</Link>
              </li>
              <li>
                <Link to="/viewer">Viewer View</Link>
              </li>
            </>
          )}

          {/* Admin Limited */}
          {role === "ADMIN_LIMITED" && (
            <>
              <li>
                <Link to="/admin-limited">Admin Limited</Link>
              </li>
              <li>
                <Link to="/viewer">Viewer View</Link>
              </li>
            </>
          )}

          {/* Agent */}
          {role === "AGENT" && (
            <li>
              <Link to="/agent">Agent View</Link>
            </li>
          )}

          {/* Viewer */}
          {role === "VIEWER" && (
            <li>
              <Link to="/viewer">Viewer View</Link>
            </li>
          )}
        </ul>
      </nav>
      <button onClick={logout} style={{ marginTop: "2rem" }}>
        Logout
      </button>
    </div>
  );
};

export default Sidebar;
