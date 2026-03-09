import React, { useState } from "react";
import { register } from "../api";

export default function Register({ onRegister, onSwitch }) {
  const [form, setForm] = useState({ username: "", email: "", first_name: "", last_name: "", phone: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await register(form);
      onRegister(res.data);
    } catch (err) {
      const detail = err.response?.data;
      setError(detail ? (typeof detail === "string" ? detail : JSON.stringify(detail)) : "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1 style={{ marginBottom: 20, textAlign: "center" }}>Create Account</h1>
      {error && <div className="alert alert-error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <div className="form-group">
            <label>First Name</label>
            <input required value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
          </div>
          <div className="form-group">
            <label>Last Name</label>
            <input required value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
          </div>
        </div>
        <div className="form-group">
          <label>Username</label>
          <input required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        </div>
        <div className="form-group">
          <label>Phone (optional)</label>
          <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" required minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        </div>
        <button type="submit" className="btn btn-success" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Creating account…" : "Register"}
        </button>
      </form>
      <p style={{ textAlign: "center", marginTop: 16, fontSize: "0.9rem" }}>
        Already have an account?{" "}
        <button onClick={onSwitch} style={{ background: "none", border: "none", color: "#2980b9", cursor: "pointer", textDecoration: "underline", fontSize: "0.9rem" }}>
          Sign In
        </button>
      </p>
    </div>
  );
}
