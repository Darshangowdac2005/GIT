import axios from "axios";

const client = axios.create({ baseURL: "/api" });

export const api = {
  setAuth(token: string | null) {
    if (token) client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    else delete client.defaults.headers.common["Authorization"];
  },
  async login(email: string, password: string) {
    const res = await client.post("/auth/login", { email, password });
    return res.data as { message: string; token: string; role: string; user_id: number };
  },
  async signup(name: string, email: string, password: string, role: string = "student") {
    const res = await client.post("/auth/signup", { name, email, password, role });
    return res.data;
  },
  async listItems(params: { status?: string; search?: string } = {}) {
    const res = await client.get("/items", { params });
    return res.data as any[];
  },
  async reportItem(payload: { title: string; description: string; status: string; category_id: number }) {
    const res = await client.post("/items", payload);
    return res.data;
  },
  async claimItem(itemId: number, verification_details: string) {
    const res = await client.post(`/items/${itemId}/claim`, { verification_details });
    return res.data;
  },
  async listCategories() {
    const res = await client.get("/categories");
    return res.data as { category_id: number; name: string }[];
  },
  async adminListPendingClaims() {
    const res = await client.get("/admin/claims/pending");
    return res.data as any[];
  },
  async adminResolveClaim(claim_id: number, resolution_type: "approve" | "reject") {
    const res = await client.post("/admin/claims/resolve", { claim_id, resolution_type });
    return res.data;
  },
  async adminCreateCategory(name: string) {
    const res = await client.post("/admin/categories", { name });
    return res.data;
  },
  async adminUpdateCategory(category_id: number, name: string) {
    const res = await client.put(`/admin/categories/${category_id}`, { name });
    return res.data;
  },
  async adminDeleteCategory(category_id: number) {
    const res = await client.delete(`/admin/categories/${category_id}`);
    return res.data;
  }
};
