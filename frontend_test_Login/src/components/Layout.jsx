// src/components/Layout.js
import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

const Layout = () => {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <main style={{ flexGrow: 1, padding: "20px" }}>
        <Outlet /> {/* << ส่วนนี้จะแสดงเนื้อหาของแต่ละหน้า */}
      </main>
    </div>
  );
};

export default Layout;
