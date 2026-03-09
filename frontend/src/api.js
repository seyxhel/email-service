import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "/api",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

// Attach Django CSRF token to every mutating request
API.interceptors.request.use((config) => {
  const csrfToken = getCookie("csrftoken");
  if (csrfToken && ["post", "put", "patch", "delete"].includes(config.method)) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? match[2] : null;
}

// ---------- Auth ----------
export const register   = (data)     => API.post("/auth/register/", data);
export const login      = (data)     => API.post("/auth/login/", data);
export const logout     = ()         => API.post("/auth/logout/");
export const getMe      = ()         => API.get("/auth/me/");

// ---------- Customers (staff) ----------
export const getCustomers = (search = "") => API.get("/customers/", { params: { search } });

// ---------- Messages ----------
export const getInbox       = ()     => API.get("/inbox/");
export const getMessage     = (id)   => API.get(`/messages/${id}/`);
export const sendMessage    = (data) => API.post("/send-message/", data);

// ---------- Meta ----------
export const getWarningTypes = () => API.get("/warning-types/");
export const getStats        = () => API.get("/stats/");

export default API;
