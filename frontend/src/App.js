import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import Customers from "./components/Customers";
import Warnings from "./components/Warnings";
import SendWarning from "./components/SendWarning";

const PAGES = {
  dashboard: "Dashboard",
  customers: "Customers",
  warnings:  "Warning Log",
  send:      "Send Warning",
};

function App() {
  const [page, setPage] = useState("dashboard");

  const renderPage = () => {
    switch (page) {
      case "customers": return <Customers />;
      case "warnings":  return <Warnings />;
      case "send":      return <SendWarning />;
      default:          return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <nav className="sidebar">
        <h2>⚠️ Warning System</h2>
        {Object.entries(PAGES).map(([key, label]) => (
          <button
            key={key}
            className={page === key ? "active" : ""}
            onClick={() => setPage(key)}
          >
            {label}
          </button>
        ))}
      </nav>
      <main className="main">{renderPage()}</main>
    </div>
  );
}

export default App;
