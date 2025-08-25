import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/api";

export default function ClientsPage() {
  const [items, setItems] = useState([]);
  const [err, setErr] = useState(null);

  const refresh = async () => {
    try { const r = await api.get("/clients/summary"); setItems(r.data); setErr(null); }
    catch (e) { setErr("Failed to load clients"); }
  };

  useEffect(() => { refresh(); }, []);

  return (
    <section className="page">
      <header className="page__header">
        <h2>Clients</h2>
        <Link className="btn" to="new">+ Add Client</Link>
      </header>
      {err && <p className="text-red-600">{err}</p>}
      <table className="table">
        <thead><tr><th>Name</th><th>Email</th><th>Phone</th><th>Status</th><th>Vehicle</th><th>Days</th></tr></thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id}>
              <td>{c.first_name} {c.last_name}</td>
              <td>{c.email}</td>
              <td>{c.phone || "-"}</td>
              <td>{c.status}</td>
              <td>{c.current_vehicle_id ?? "-"}</td>
              <td>{c.days_with_vehicle}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
