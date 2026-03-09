import React, { useState } from "react";
import { login } from "../api";

export default function Login({ onLogin, onSwitch }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login(form);
      onLogin(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1 style={{ marginBottom: 20, textAlign: "center" }}>Sign In</h1>
      {error && <div className="alert alert-error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        </div>
        <button type="submit" className="btn btn-primary" style={{ width: "100%" }} disabled={loading}>
          {loading ? "Signing in…" : "Sign In"}
        </button>
      </form>
      <p style={{ textAlign: "center", marginTop: 16, fontSize: "0.9rem" }}>
        Don't have an account?{" "}
        <button onClick={onSwitch} style={{ background: "none", border: "none", color: "#2980b9", cursor: "pointer", textDecoration: "underline", fontSize: "0.9rem" }}>
          Register
        </button>
      </p>
    </div>
  );
}
