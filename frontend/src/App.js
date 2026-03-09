import React, { useState, useEffect, useCallback } from "react";
import { getMe, logout as apiLogout } from "./api";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import Customers from "./components/Customers";
import SendWarning from "./components/SendWarning";
import Inbox from "./components/Inbox";
import MessageView from "./components/MessageView";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState("inbox");
  const [authPage, setAuthPage] = useState("login");
  const [selectedMessageId, setSelectedMessageId] = useState(null);

  const checkAuth = useCallback(() => {
    getMe()
      .then((r) => { setUser(r.data); setLoading(false); })
      .catch(() => { setUser(null); setLoading(false); });
  }, []);

  useEffect(() => { checkAuth(); }, [checkAuth]);

  const handleLogout = async () => {
    await apiLogout().catch(() => {});
    setUser(null);
    setPage("inbox");
    setSelectedMessageId(null);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setPage("inbox");
  };

  const openMessage = (id) => {
    setSelectedMessageId(id);
    setPage("message");
  };

  if (loading) return <div className="app"><main className="main"><p>Loading…</p></main></div>;

  // ---------- Not logged in ----------
  if (!user) {
    return (
      <div className="app">
        <main className="main" style={{ maxWidth: 440, margin: "60px auto" }}>
          {authPage === "login" ? (
            <Login onLogin={handleLogin} onSwitch={() => setAuthPage("register")} />
          ) : (
            <Register onRegister={handleLogin} onSwitch={() => setAuthPage("login")} />
          )}
        </main>
      </div>
    );
  }

  // ---------- Logged in ----------
  const isStaff = user.role === "staff";

  const PAGES = isStaff
    ? { dashboard: "Dashboard", customers: "Customers", inbox: "Sent Messages", send: "Send Warning" }
    : { inbox: "Inbox" };

  const renderPage = () => {
    if (page === "message" && selectedMessageId) {
      return <MessageView messageId={selectedMessageId} onBack={() => setPage("inbox")} />;
    }
    switch (page) {
      case "dashboard": return isStaff ? <Dashboard /> : null;
      case "customers": return isStaff ? <Customers /> : null;
      case "send":      return isStaff ? <SendWarning /> : null;
      default:          return <Inbox user={user} onOpenMessage={openMessage} />;
    }
  };

  return (
    <div className="app">
      <nav className="sidebar">
        <h2>📧 Warning System</h2>
        <p style={{ fontSize: "0.8rem", opacity: 0.7, marginBottom: 16, textAlign: "center" }}>
          {user.full_name || user.username}<br />
          <span className="badge" style={{ background: isStaff ? "#2980b9" : "#27ae60", color: "#fff" }}>
            {user.role}
          </span>
        </p>
        {Object.entries(PAGES).map(([key, label]) => (
          <button key={key} className={page === key ? "active" : ""} onClick={() => { setPage(key); setSelectedMessageId(null); }}>
            {label}
          </button>
        ))}
        <button onClick={handleLogout} style={{ marginTop: 20, color: "#e74c3c" }}>Logout</button>
      </nav>
      <main className="main">{renderPage()}</main>
    </div>
  );
}

export default App;
