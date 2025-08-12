import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import VehiclesPage from "./pages/VehiclesPage";
import ClientsPage from "./pages/ClientsPage";
import RemindersPage from "./pages/RemindersPage";
import "./styles/dashboard.css";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <h1 className="navbar__brand">Fleet Pro</h1>
        <div className="navbar__links">
          <Link to="/">Dashboard</Link>
          <Link to="/vehicles">Vehicles</Link>
          <Link to="/clients">Clients</Link>
          <Link to="/reminders">Reminders</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/vehicles/*" element={<VehiclesPage />} />
        <Route path="/clients/*" element={<ClientsPage />} />
        <Route path="/reminders/*" element={<RemindersPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
