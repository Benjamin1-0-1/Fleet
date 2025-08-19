import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/api";

export default function VehicleList() {
  const [vehicles, setVehicles] = useState([]);
  const navigate = useNavigate();

  const refresh = () => api.get("/vehicles").then((r) => setVehicles(r.data));


  useEffect(() => {
  (async () => {
    try {
      const r = await api.get("/vehicles");
      setVehicles(r.data);
    } catch (err) {
      console.error("[VehicleList] load failed:", err?.message || err);
      setVehicles([]); // fail soft
    }
  })();
}, []);

  const remove = async (id) => {
    if (window.confirm("Delete this vehicle?")) {
      await api.delete(`/vehicles/${id}`);
      refresh();
    }
  };

  return (
    <section className="page">
      <header className="page__header">
        <h2>Vehicles</h2>
        <Link className="btn" to="new">+ Add Vehicle</Link>
      </header>
      <ul className="cards">
        {vehicles.map((v) => (
          <li key={v.id} className="card">
            <div><strong>{v.plate}</strong> — {v.make} {v.model} ({v.v_class})</div>
            <div className="card__actions">
              <button onClick={() => navigate(`${v.id}/edit`)}>Edit</button>
              <button className="danger" onClick={() => remove(v.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
