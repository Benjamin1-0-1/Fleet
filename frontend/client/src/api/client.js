import axios from "axios";

// Point this to your Flask server
const BASE_URL = process.env.REACT_APP_API_BASE || "http://localhost:5000";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" }
});

// Helper CRUD shortcuts
export const getAll = (path) => api.get(path).then(r => r.data);
export const getOne = (path) => api.get(path).then(r => r.data);
export const createOne = (path, data) => api.post(path, data).then(r => r.data);
export const replaceOne = (path, data) => api.put(path, data).then(r => r.data);
export const patchOne = (path, data) => api.patch(path, data).then(r => r.data);
export const deleteOne = (path) => api.delete(path).then(r => r.data);
