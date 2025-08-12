import { useEffect, useState } from "react";
import api from "../api/api";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [summary, setSummary] = useState({ vehicles: 0, total_costs: 0 });

  useEffect(() => {
    api.get("/analytics/summary").then((r) => setSummary(r.data));
  }, []);

  return (
    <section className="page">
      <header className="page__header"><h2>Dashboard</h2></header>
      <div className="stats">
        <div className="stat">
          <div className="stat__num">{summary.vehicles}</div>
          <div className="stat__label">Vehicles</div>
        </div>
        <div className="stat">
          <div className="stat__num">${summary.total_costs?.toFixed?.(2) || 0}</div>
          <div className="stat__label">Total Costs</div>
        </div>
      </div>
    </section>
  );
}
