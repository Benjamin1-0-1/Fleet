import axios from "axios";

/**
 * Dev: CRA proxy forwards "/api" -> "http://localhost:5000"
 * Prod (or if you remove proxy): set REACT_APP_API_URL to your backend URL.
 */
const baseURL =
  (process.env.REACT_APP_API_URL && process.env.REACT_APP_API_URL.trim()) ||
  "/api";

const api = axios.create({ baseURL });
export default api;
