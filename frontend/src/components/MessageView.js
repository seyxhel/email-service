import React, { useEffect, useState } from "react";
import { getMessage } from "../api";

export default function MessageView({ messageId, onBack }) {
  const [msg, setMsg] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getMessage(messageId)
      .then((r) => setMsg(r.data))
      .catch(() => setError("Failed to load message."));
  }, [messageId]);

  if (error) return <div className="alert alert-error">{error}</div>;
  if (!msg) return <p>Loading…</p>;

  return (
    <>
      <button className="btn btn-primary" onClick={onBack} style={{ marginBottom: 20 }}>
        ← Back
      </button>

      <div className="card">
        <div style={{ borderBottom: "1px solid #ecf0f1", paddingBottom: 16, marginBottom: 16 }}>
          <h1 style={{ marginBottom: 8 }}>{msg.subject}</h1>
          <div style={{ display: "flex", gap: 24, fontSize: "0.9rem", color: "#7f8c8d" }}>
            <span><strong>From:</strong> {msg.sender_name}</span>
            <span><strong>To:</strong> {msg.recipient_name}</span>
            <span><strong>Type:</strong> {msg.warning_type_display}</span>
            <span><strong>Date:</strong> {new Date(msg.created_at).toLocaleString()}</span>
          </div>
          {msg.is_read && msg.read_at && (
            <div style={{ fontSize: "0.8rem", color: "#27ae60", marginTop: 4 }}>
              ✓ Read on {new Date(msg.read_at).toLocaleString()}
            </div>
          )}
        </div>

        <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.7, fontSize: "1rem" }}>
          {msg.body}
        </div>
      </div>
    </>
  );
}
