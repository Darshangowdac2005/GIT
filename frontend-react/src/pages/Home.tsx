import React, { useEffect, useState } from "react";
import { api } from "../utils/api";

export default function Home() {
  const [status, setStatus] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    try {
      const data = await api.listItems({ status: status || undefined, search: search || undefined });
      setItems(data || []);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h2>Lost &amp; Found Listings</h2>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <input placeholder="Search" value={search} onChange={(e) => setSearch(e.target.value)} />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All</option>
          <option value="lost">Lost</option>
          <option value="found">Found</option>
        </select>
        <button onClick={load}>Search</button>
      </div>

      <div style={{ marginTop: 16 }}>
        {loading ? (
          <div>Loading...</div>
        ) : items.length === 0 ? (
          <div>No items found.</div>
        ) : (
          <ul style={{ listStyle: "none", padding: 0, display: "grid", gap: 12 }}>
            {items.map((it) => (
              <li key={it.item_id} style={{ border: "1px solid #ddd", padding: 12, borderRadius: 6 }}>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <strong>{it.title}</strong>
                  <span style={{ background: it.status === "found" ? "#1b5e20" : "#b71c1c", color: "white", borderRadius: 4, padding: "2px 8px" }}>{(it.status || "").toUpperCase()}</span>
                </div>
                <div>Category: {it.category_name || "N/A"}</div>
                <div>{it.description || ""}</div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
