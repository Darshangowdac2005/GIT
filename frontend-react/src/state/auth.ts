import { useEffect, useState } from "react";
import { api } from "../utils/api";

export function useAuth() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("auth_token"));
  const [role, setRole] = useState<string | null>(() => localStorage.getItem("auth_role"));

  useEffect(() => {
    if (token) localStorage.setItem("auth_token", token); else localStorage.removeItem("auth_token");
  }, [token]);

  useEffect(() => {
    if (role) localStorage.setItem("auth_role", role); else localStorage.removeItem("auth_role");
  }, [role]);

  function login(newToken: string, newRole: string) {
    setToken(newToken);
    setRole((newRole ?? "").toLowerCase());
    api.setAuth(newToken);
  }

  function logout() {
    setToken(null);
    setRole(null);
    api.setAuth(null);
  }

  return { token, role, login, logout };
}
