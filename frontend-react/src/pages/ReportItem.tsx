import React, { useEffect, useState } from "react";
import { api } from "../utils/api";

export default function ReportItem() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("lost");
  const [categories, setCategories] = useState<{ category_id: number; name: string }[]>([]);
  const [categoryId, setCategoryId] = useState<number | "">("");
  const [msg, setMsg] = useState("");

  useEffect(() => {
    api.listCategories().then(setCategories).catch(() => setCategories([]));
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!title || !description || !status || !categoryId) return setMsg("All fields required");
    setMsg("Submitting...");
    try {
      const res = await api.reportItem({ title, description, status, category_id: Number(categoryId) });
      if (res?.id) setMsg("Reported successfully"); else setMsg(res?.error || "Report failed");
    } catch (err: any) {
      setMsg(err?.response?.data?.error || "Report failed");
    }
  }

  return (
    <form onSubmit={submit} style={{ maxWidth: 500 }}>
      <h2>Report Item</h2>
      <div>
        <label>Status: </label>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="lost">I Lost This Item</option>
          <option value="found">I Found This Item</option>
        </select>
      </div>
      <input placeholder="Item Name" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="Detailed Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <select value={categoryId} onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : "")} disabled={categories.length === 0}>
        <option value="">Select Category</option>
        {categories.map((c) => (
          <option key={c.category_id} value={c.category_id}>{c.name}</option>
        ))}
      </select>
      <button type="submit">Submit Report</button>
      <div>{msg}</div>
    </form>
  );
}
