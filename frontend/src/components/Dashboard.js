import React, { useEffect, useState } from "react";
import { getStats } from "../api";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getStats()
      .then((res) => setStats(res.data))
      .catch(() => setError("Failed to load dashboard stats. Make sure you are logged in."));
  }, []);

  if (error) return <div className="alert alert-error">{error}</div>;
  if (!stats) return <p>Loading…</p>;

  return (
    <>
      <div className="section-header"><h1>Dashboard</h1></div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{stats.total_customers}</h3>
          <p>Customers</p>
        </div>
        <div className="stat-card">
          <h3>{stats.total_warnings}</h3>
          <p>Total Warnings</p>
        </div>
        <div className="stat-card">
          <h3>{stats.sent}</h3>
          <p>Sent</p>
        </div>
        <div className="stat-card">
          <h3>{stats.pending}</h3>
          <p>Pending</p>
        </div>
        <div className="stat-card">
          <h3>{stats.failed}</h3>
          <p>Failed</p>
        </div>
      </div>

      {stats.by_type.length > 0 && (
        <div className="card">
          <h2 style={{ marginBottom: 12 }}>Warnings by Type</h2>
          <table>
            <thead>
              <tr><th>Type</th><th>Count</th></tr>
            </thead>
            <tbody>
              {stats.by_type.map((t) => (
                <tr key={t.warning_type}>
                  <td>{t.warning_type}</td>
                  <td>{t.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
