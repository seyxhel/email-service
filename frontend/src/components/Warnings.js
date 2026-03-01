import React, { useEffect, useState, useCallback } from "react";
import { getWarnings } from "../api";

function StatusBadge({ status }) {
  const cls = status === "sent" ? "badge-sent" : status === "failed" ? "badge-failed" : "badge-pending";
  return <span className={`badge ${cls}`}>{status}</span>;
}

export default function Warnings() {
  const [warnings, setWarnings] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(() => {
    getWarnings(search)
      .then((r) => setWarnings(r.data.results || r.data))
      .catch(() => setError("Failed to load warnings."));
  }, [search]);

  useEffect(() => { load(); }, [load]);

  return (
    <>
      <div className="section-header"><h1>Warning Log</h1></div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="form-group" style={{ maxWidth: 350 }}>
        <input placeholder="Search warnings…" value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th><th>Customer</th><th>Type</th><th>Subject</th>
            <th>Status</th><th>Sent By</th><th>Date</th>
          </tr>
        </thead>
        <tbody>
          {warnings.length === 0 ? (
            <tr><td colSpan={7} style={{ textAlign: "center" }}>No warning records.</td></tr>
          ) : (
            warnings.map((w) => (
              <tr key={w.id}>
                <td>{w.id}</td>
                <td>{w.customer_name}<br/><small>{w.customer_email}</small></td>
                <td>{w.warning_type_display}</td>
                <td>{w.subject}</td>
                <td><StatusBadge status={w.status} /></td>
                <td>{w.sent_by || "—"}</td>
                <td>{w.sent_at ? new Date(w.sent_at).toLocaleString() : "—"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}
