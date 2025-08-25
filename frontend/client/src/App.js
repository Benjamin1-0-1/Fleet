import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import VehiclesPage from "./pages/VehiclesPage";
import VehicleDetail from "./pages/VehicleDetail";
import ClientsPage from "./pages/ClientsPage";
import RemindersPage from "./pages/RemindersPage";
import Login from "./pages/Login";
import ThemeToggle from "./components/ThemeToggle";
import LogoutButton from "./components/LogoutButton";
import "./index.css";

export default function App() {
  const token = localStorage.getItem("vm_token");
  return (
    <BrowserRouter>
      <nav className="navbar">
        <h1 className="navbar__brand">Fleet Pro</h1>
        <div className="navbar__links">
          <Link to="/">Dashboard</Link>
          <Link to="/vehicles">Vehicles</Link>
          <Link to="/clients">Clients</Link>
          <Link to="/reminders">Reminders</Link>
          <ThemeToggle />
          {token ? <LogoutButton /> : <Link className="btn-outline" to="/login">Login</Link>}
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/vehicles/*" element={<VehiclesPage />} />
        <Route path="/vehicles/:id" element={<VehicleDetail />} />
        <Route path="/clients/*" element={<ClientsPage />} />
        <Route path="/reminders/*" element={<RemindersPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
