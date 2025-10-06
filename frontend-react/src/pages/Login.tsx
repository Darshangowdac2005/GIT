import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../utils/api";
import { useAuth } from "../state/auth";

export default function Login() {
  const nav = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("Logging in...");
    try {
      const res = await api.login(email, password);
      login(res.token, res.role);
      setMsg("Success");
      nav("/");
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Login failed");
    }
  }

  return (
    <form onSubmit={submit} style={{ maxWidth: 380 }}>
      <h2>Login</h2>
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
      <div>{msg}</div>
    </form>
  );
}
