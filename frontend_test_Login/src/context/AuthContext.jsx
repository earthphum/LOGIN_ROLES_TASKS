// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // ตรวจสอบ user ตอนเปิดแอปครั้งแรก
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchUserDetails();
    }
  }, []);

  const fetchUserDetails = async () => {
    try {
      const response = await api.get("/users/me/");
      setUser(response.data);
    } catch (error) {
      console.error("Could not fetch user details", error);
      logout(); // ถ้า token หมดอายุหรือใช้ไม่ได้ ให้ logout
    }
  };

  const login = async (username, password) => {
    try {
      const response = await api.post("/token/", { username, password });
      localStorage.setItem("access_token", response.data.access);
      await fetchUserDetails(); // ดึงข้อมูล user หลัง login สำเร็จ
      navigate("/dashboard"); // ไปยังหน้า dashboard
    } catch (error) {
      console.error("Login failed", error);
      throw new Error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง");
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("access_token");
    navigate("/");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook เพื่อให้เรียกใช้ง่าย
export const useAuth = () => {
  return useContext(AuthContext);
};
