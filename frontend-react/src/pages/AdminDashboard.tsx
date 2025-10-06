import React, { useEffect, useState } from "react";
import { api } from "../utils/api";

export default function AdminDashboard() {
  const [claims, setClaims] = useState<any[]>([]);
  const [catName, setCatName] = useState("");
  const [categories, setCategories] = useState<{ category_id: number; name: string }[]>([]);
  const [msg, setMsg] = useState("");

  async function loadClaims() {
    try {
      const data = await api.adminListPendingClaims();
      setClaims(data || []);
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Failed to load claims");
    }
  }

  async function loadCategories() {
    try {
      const data = await api.listCategories();
      setCategories(data || []);
    } catch {
      setCategories([]);
    }
  }

  useEffect(() => {
    loadClaims();
    loadCategories();
  }, []);

  async function resolveClaim(id: number, type: "approve" | "reject") {
    try {
      await api.adminResolveClaim(id, type);
      setMsg(`Claim ${type}d`);
      await loadClaims();
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Resolution failed");
    }
  }

  async function createCategory() {
    if (!catName.trim()) return setMsg("Enter category name");
    try {
      await api.adminCreateCategory(catName.trim());
      setCatName("");
      await loadCategories();
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Create failed");
    }
  }

  async function updateCategory(id: number, name: string) {
    const newName = prompt("New name", name) || "";
    if (!newName.trim()) return;
    try {
      await api.adminUpdateCategory(id, newName.trim());
      await loadCategories();
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Update failed");
    }
  }

  async function deleteCategory(id: number) {
    if (!confirm("Delete category?")) return;
    try {
      await api.adminDeleteCategory(id);
      await loadCategories();
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Delete failed");
    }
  }

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <div style={{ color: "#b71c1c" }}>{msg}</div>

      <section>
        <h3>Claims Management</h3>
        {claims.length === 0 ? (
          <div>No claims to review</div>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Item</th>
                <th>Claimant</th>
                <th>Verification</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {claims.map((c) => (
                <tr key={c.claim_id}>
                  <td>{c.claim_id}</td>
                  <td>{c.item_title}</td>
                  <td>{c.claimant_name} ({c.claimant_email})</td>
                  <td>{c.verification_details}</td>
                  <td>
                    <button onClick={() => resolveClaim(c.claim_id, "approve")}>Approve</button>
                    <button onClick={() => resolveClaim(c.claim_id, "reject")}>Reject</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>Manage Categories</h3>
        <div style={{ display: "flex", gap: 8 }}>
          <input placeholder="New category" value={catName} onChange={(e) => setCatName(e.target.value)} />
          <button onClick={createCategory}>Add</button>
        </div>
        <table style={{ width: "100%", borderCollapse: "collapse", marginTop: 12 }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((cat) => (
              <tr key={cat.category_id}>
                <td>{cat.category_id}</td>
                <td>{cat.name}</td>
                <td>
                  <button onClick={() => updateCategory(cat.category_id, cat.name)}>Edit</button>
                  <button onClick={() => deleteCategory(cat.category_id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
