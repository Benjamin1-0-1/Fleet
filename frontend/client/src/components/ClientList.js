import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/api";

export default function ClientList() {
  const [items, setItems] = useState([]);
  const navigate = useNavigate();

  const refresh = () => api.get("/clients").then((r) => setItems(r.data));
  useEffect(refresh, []);

  const remove = async (id) => {
    if (window.confirm("Delete this client?")) {
      await api.delete(`/clients/${id}`);
      refresh();
    }
  };

  return (
    <section className="page">
      <header className="page__header">
        <h2>Clients</h2>
        <Link className="btn" to="new">+ Add Client</Link>
      </header>
      <ul className="cards">
        {items.map((c) => (
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
