import React, { useEffect, useState, useCallback } from "react";
import { getCustomers } from "../api";

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(() => {
    getCustomers(search)
      .then((r) => setCustomers(r.data))
      .catch(() => setError("Failed to load customers."));
  }, [search]);

  useEffect(() => { load(); }, [load]);

  return (
    <>
      <div className="section-header"><h1>Customers</h1></div>
      {error && <div className="alert alert-error">{error}</div>}

      <div className="form-group" style={{ maxWidth: 350 }}>
        <input placeholder="Search customers…" value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Username</th><th>Email</th><th>Phone</th><th>Joined</th></tr>
        </thead>
        <tbody>
          {customers.length === 0 ? (
            <tr><td colSpan={6} style={{ textAlign: "center" }}>No customers found.</td></tr>
          ) : (
            customers.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.first_name} {c.last_name}</td>
                <td>{c.username}</td>
                <td>{c.email}</td>
                <td>{c.phone || "—"}</td>
                <td>{new Date(c.date_joined).toLocaleDateString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}
