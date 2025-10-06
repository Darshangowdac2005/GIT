import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../utils/api";

export default function Signup() {
  const nav = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [msg, setMsg] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!name || !email || !password || !confirm) return setMsg("All fields required");
    if (password !== confirm) return setMsg("Passwords do not match");
    setMsg("Signing up...");
    try {
      await api.signup(name, email, password);
      setMsg("Signup successful");
      nav("/login");
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Signup failed");
    }
  }

  return (
    <form onSubmit={submit} style={{ maxWidth: 380 }}>
      <h2>Signup</h2>
      <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <input placeholder="Confirm Password" type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} />
      <button type="submit">Signup</button>
      <div>{msg}</div>
    </form>
  );
}
