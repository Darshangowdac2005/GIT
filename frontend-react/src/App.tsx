import React from "react";
import { Routes, Route, Navigate, Link } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ReportItem from "./pages/ReportItem";
import AdminDashboard from "./pages/AdminDashboard";
import { useAuth } from "./state/auth";

export default function App() {
  const { token, role, logout } = useAuth();
  const isAdmin = (role ?? "").toLowerCase() === "admin";

  return (
    <div style={{ fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Arial", color: "#111" }}>
      <nav style={{ display: "flex", gap: 12, padding: 12, background: "#0d47a1", color: "white" }}>
        <Link to="/" style={{ color: "white", textDecoration: "none", fontWeight: 700 }}>Back2U Portal</Link>
        <div style={{ flex: 1 }} />
        <Link to="/" style={{ color: "white", textDecoration: "none" }}>Home</Link>
        {token && <Link to="/report" style={{ color: "white", textDecoration: "none" }}>Report Item</Link>}
        {token && isAdmin && <Link to="/admin" style={{ color: "white", textDecoration: "none" }}>Admin</Link>}
        {!token && <Link to="/signup" style={{ color: "white", textDecoration: "none" }}>Signup</Link>}
        {!token && <Link to="/login" style={{ color: "white", textDecoration: "none" }}>Login</Link>}
        {token && <button onClick={logout} style={{ color: "#0d47a1", background: "white", border: 0, borderRadius: 4, padding: "4px 10px" }}>Logout</button>}
      </nav>

      <div style={{ padding: 16 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/report" element={token ? <ReportItem /> : <Navigate to="/login" replace />} />
          <Route path="/admin" element={token && isAdmin ? <AdminDashboard /> : <Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  );
}
