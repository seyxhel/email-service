import React, { useEffect, useState, useCallback } from "react";
import { getInbox } from "../api";

export default function Inbox({ user, onOpenMessage }) {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");

  const load = useCallback(() => {
    getInbox()
      .then((r) => setMessages(r.data))
      .catch(() => setError("Failed to load messages."));
  }, []);

  useEffect(() => { load(); }, [load]);

  const isStaff = user.role === "staff";

  return (
    <>
      <div className="section-header">
        <h1>{isStaff ? "Sent Messages" : "Inbox"}</h1>
      </div>
      {error && <div className="alert alert-error">{error}</div>}

      <table>
        <thead>
          <tr>
            <th></th>
            <th>{isStaff ? "To" : "From"}</th>
            <th>Type</th>
            <th>Subject</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {messages.length === 0 ? (
            <tr><td colSpan={5} style={{ textAlign: "center" }}>No messages yet.</td></tr>
          ) : (
            messages.map((m) => (
              <tr
                key={m.id}
                onClick={() => onOpenMessage(m.id)}
                style={{ cursor: "pointer", fontWeight: !isStaff && !m.is_read ? 700 : 400 }}
              >
                <td style={{ width: 30 }}>
                  {!isStaff && !m.is_read && <span style={{ color: "#2980b9", fontSize: "1.2rem" }}>●</span>}
                </td>
                <td>{isStaff ? m.recipient_name : m.sender_name}</td>
                <td><span className="badge badge-pending">{m.warning_type_display}</span></td>
                <td>{m.subject}</td>
                <td>{new Date(m.created_at).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}
