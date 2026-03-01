import axios from "axios";

// In development the React dev-server proxies /api to Django (see package.json "proxy").
// In production, set REACT_APP_API_URL to the Django backend URL.
const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "/api",
  withCredentials: true,       // send session cookie
  headers: { "Content-Type": "application/json" },
});

// ---------- Customers ----------
export const getCustomers  = (search = "")  => API.get(`/customers/`, { params: { search } });
export const getCustomer   = (id)           => API.get(`/customers/${id}/`);
export const createCustomer = (data)        => API.post(`/customers/`, data);
export const updateCustomer = (id, data)    => API.put(`/customers/${id}/`, data);
export const deleteCustomer = (id)          => API.delete(`/customers/${id}/`);

// ---------- Warnings ----------
export const getWarnings       = (search = "") => API.get(`/warnings/`, { params: { search } });
export const getCustomerWarnings = (id)        => API.get(`/customers/${id}/warnings/`);
export const sendWarning       = (data)        => API.post(`/send-warning/`, data);

// ---------- Meta ----------
export const getWarningTypes = () => API.get(`/warning-types/`);
export const getStats        = () => API.get(`/stats/`);

export default API;
