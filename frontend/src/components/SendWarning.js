import React, { useEffect, useState } from "react";
import { getCustomers, getWarningTypes, sendMessage } from "../api";

export default function SendWarning() {
  const [customers, setCustomers] = useState([]);
  const [types, setTypes] = useState([]);
  const [form, setForm] = useState({ recipient_id: "", warning_type: "", subject: "", body: "" });
  const [sending, setSending] = useState(false);
  const [msg, setMsg] = useState({ type: "", text: "" });

  useEffect(() => {
    getCustomers().then((r) => setCustomers(r.data)).catch(() => {});
    getWarningTypes().then((r) => setTypes(r.data)).catch(() => {});
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSending(true);
    setMsg({ type: "", text: "" });
    try {
      await sendMessage({ ...form, recipient_id: Number(form.recipient_id) });
      setMsg({ type: "success", text: "Warning message sent successfully!" });
      setForm({ recipient_id: "", warning_type: "", subject: "", body: "" });
    } catch (err) {
      const detail = err.response?.data;
      setMsg({ type: "error", text: detail ? JSON.stringify(detail) : "Error sending message." });
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <div className="section-header"><h1>Send Warning</h1></div>

      {msg.text && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div className="form-group">
              <label>Customer</label>
              <select required value={form.recipient_id} onChange={(e) => setForm({ ...form, recipient_id: e.target.value })}>
                <option value="">— select customer —</option>
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>{c.first_name} {c.last_name} ({c.username})</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Warning Type</label>
              <select required value={form.warning_type} onChange={(e) => setForm({ ...form, warning_type: e.target.value })}>
                <option value="">— select type —</option>
                {types.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="form-group">
            <label>Subject</label>
            <input required value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} />
          </div>
          <div className="form-group">
            <label>Message</label>
            <textarea required value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} />
          </div>
          <button type="submit" className="btn btn-danger" disabled={sending}>
            {sending ? "Sending…" : "Send Warning"}
          </button>
        </form>
      </div>
    </>
  );
}
