import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/api";

export default function ClientList() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const refresh = async () => {
    try {
      const r = await api.get("/clients");
      setClients(r.data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to fetch clients");
      console.error("[ClientList] load failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const r = await api.get("/clients");
        if (alive) {
          setClients(r.data);
          setError(null);
        }
      } catch (err) {
        if (alive) setError(err.message || "Failed to fetch clients");
        console.error("[ClientList] initial load failed:", err);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  const remove = async (id) => {
    if (!window.confirm("Delete this client?")) return;
    try {
      await api.delete(`/clients/${id}`);
      await refresh();
    } catch (err) {
      console.error("[ClientList] delete failed:", err);
      alert("Failed to delete client.");
    }
  };

  if (loading) return <section className="page"><p>Loading clients...</p></section>;
  if (error) return <section className="page"><p className="error">{error}</p></section>;

  return (
    <section className="page">
      <header className="page__header">
        <h2>Clients</h2>
        <Link className="btn" to="new">+ Add Client</Link>
      </header>
      <ul className="cards">
        {clients.map((c) => (
          <li key={c.id} className="card">
            <div><strong>{c.first_name} {c.last_name}</strong> — {c.email}</div>
            <div className="card__actions">
              <button onClick={() => navigate(`${c.id}/edit`)}>Edit</button>
              <button className="danger" onClick={() => remove(c.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
