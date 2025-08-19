import axios from "axios";

const api = axios.create({
  baseURL: "/api",                // CRA proxy will forward to :5000
  timeout: 15000,
  headers: { "Content-Type": "application/json" }
});

// helpful one-time log
if (!window.__API_BASE_LOGGED__) {
  console.log("[API] baseURL =", api.defaults.baseURL);
  window.__API_BASE_LOGGED__ = true;
}

// optional: response error logging
api.interceptors.response.use(
  (r) => r,
  (err) => {
    console.error("[API ERROR]", err?.response?.status, err?.config?.url, err?.message);
    throw err;
  }
);

export default api;
