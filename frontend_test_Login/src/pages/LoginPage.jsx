import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { user, login } = useAuth(); // ดึงสถานะ user จาก Context
  const navigate = useNavigate();

  // ใช้ useEffect เพื่อตรวจสอบสถานะ user ทุกครั้งที่ component render
  useEffect(() => {
    // ถ้าใน Context มีข้อมูล user อยู่แล้ว (หมายถึง login อยู่)
    // ให้ redirect ไปที่หน้า dashboard ทันที
    if (user) {
      navigate("/dashboard");
    }
  }, [user, navigate]); // ให้ effect นี้ทำงานเมื่อค่า user หรือ navigate เปลี่ยนไป

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(username, password);
    } catch (err) {
      setError(err.message);
    }
  };

  // ถ้ามี user อยู่แล้ว (กำลังจะ redirect) ให้แสดงข้อความ loading
  // เพื่อป้องกันไม่ให้ฟอร์มแสดงขึ้นมาชั่วครู่
  if (user) {
    return <div>กำลังตรวจสอบสถานะ...</div>;
  }

  // ถ้าไม่มี user จึงจะแสดงฟอร์ม Login
  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
