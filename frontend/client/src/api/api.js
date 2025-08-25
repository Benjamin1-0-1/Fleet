import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 15000,
  headers: { "Content-Type": "application/json" },
});

// attach token
api.interceptors.request.use((config) => {
  const t = localStorage.getItem("vm_token");
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

export default api;
