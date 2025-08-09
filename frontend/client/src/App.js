import logo from './logo.svg';
import './App.css';
import React from "react";
import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import FleetsPage from "./pages/FleetsPage";
import ClientsPage from "./pages/ClientsPage";
import RemindersPage from "./pages/RemindersPage";
import AnalyticsPage from "./pages/AnalyticsPage";


const Nav = () => (
  <nav className="bg-white shadow mb-6">
    <div className="max-w-6xl mx-auto px-4 py-3 flex gap-4">
      {[
        ["Fleets", "/fleets"],
        ["Clients", "/clients"],
        ["Reminders", "/reminders"],
        ["Analytics", "/analytics"]
      ].map(([label, to]) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `px-3 py-1 rounded ${isActive ? "bg-blue-600 text-white" : "text-gray-700 hover:bg-gray-100"}`
          }
        >
          {label}
        </NavLink>
      ))}
    </div>
  </nav>
);


export default function App() {
  return (
    <div>
      <Nav />
      <main className="max-w-6xl mx-auto px-4">
        <Routes>
          <Route path="/" element={<Navigate to="/fleets" replace />} />
          <Route path="/fleets" element={<FleetsPage />} />
          <Route path="/clients" element={<ClientsPage />} />
          <Route path="/reminders" element={<RemindersPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </main>
    </div>
  );
}

