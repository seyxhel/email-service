import React, { useEffect, useState, useCallback } from "react";
import { getCustomers, createCustomer, deleteCustomer } from "../api";

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", phone: "", notes: "" });
  const [msg, setMsg] = useState({ type: "", text: "" });

  const load = useCallback(() => {
    getCustomers(search)
      .then((r) => setCustomers(r.data.results || r.data))
      .catch(() => setMsg({ type: "error", text: "Failed to load customers." }));
  }, [search]);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createCustomer(form);
      setMsg({ type: "success", text: "Customer created." });
      setForm({ first_name: "", last_name: "", email: "", phone: "", notes: "" });
      setShowForm(false);
      load();
    } catch (err) {
      const detail = err.response?.data;
      setMsg({ type: "error", text: detail ? JSON.stringify(detail) : "Error creating customer." });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this customer?")) return;
    try {
      await deleteCustomer(id);
      setMsg({ type: "success", text: "Customer deleted." });
      load();
    } catch {
      setMsg({ type: "error", text: "Error deleting customer." });
    }
  };

  return (
    <>
      <div className="section-header">
        <h1>Customers</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Add Customer"}
        </button>
      </div>

      {msg.text && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      {showForm && (
        <div className="card">
          <form onSubmit={handleCreate}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div className="form-group">
                <label>First Name</label>
                <input required value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input required value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              </div>
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
            </div>
            <button type="submit" className="btn btn-success">Save Customer</button>
          </form>
        </div>
      )}

      <div className="form-group" style={{ maxWidth: 350 }}>
        <input
          placeholder="Search customers…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Warnings</th><th></th></tr>
        </thead>
        <tbody>
          {customers.length === 0 ? (
            <tr><td colSpan={6} style={{ textAlign: "center" }}>No customers found.</td></tr>
          ) : (
            customers.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.first_name} {c.last_name}</td>
                <td>{c.email}</td>
                <td>{c.phone || "—"}</td>
                <td>{c.warning_count}</td>
                <td><button className="btn btn-danger" style={{ padding: "4px 10px", fontSize: "0.8rem" }} onClick={() => handleDelete(c.id)}>Delete</button></td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}
