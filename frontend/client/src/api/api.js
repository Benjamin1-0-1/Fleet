import axios from "axios";

// Use explicit backend URL in dev; falls back to /api for prod.
const baseURL = process.env.REACT_APP_API_BASE || "/api";

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("vm_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
