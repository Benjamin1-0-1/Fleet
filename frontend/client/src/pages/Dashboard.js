import { useEffect, useState } from "react";
import api from "../api/api";

export default function Dashboard() {
  const [stats, setStats] = useState({
    vehicles: 0,
    total_costs: 0,
    revenue_year: 0,
    revenue_month: 0,
    revenue_week: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // ✅ define setError

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const r = await api.get("/analytics/summary"); // -> http://localhost:5000/api/analytics/summary
        if (!alive) return;
        setStats({
          vehicles: r.data.vehicles ?? 0,
          total_costs: r.data.total_costs ?? 0,
          revenue_year: r.data.revenue_year ?? 0,
          revenue_month: r.data.revenue_month ?? 0,
          revenue_week: r.data.revenue_week ?? 0,
        });
      } catch (e) {
        console.error("[Dashboard] load failed:", e);
        if (alive) setError("Failed to load dashboard.");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  return (
    <section className="page">
      <header className="page__header">
        <h2>Dashboard</h2>
      </header>

      {error && <p className="text-red-600 mb-3">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <div className="text-4xl font-bold">{stats.vehicles}</div>
          <div className="text-gray-600">Vehicles</div>
        </div>
        <div className="card">
          <div className="text-4xl font-bold">${stats.total_costs.toFixed(2)}</div>
          <div className="text-gray-600">Total Costs</div>
        </div>
        <div className="card">
          <div className="text-4xl font-bold">${stats.revenue_month.toFixed(2)}</div>
          <div className="text-gray-600">Revenue (Month)</div>
        </div>
        <div className="card">
          <div className="text-4xl font-bold">${stats.revenue_week.toFixed(2)}</div>
          <div className="text-gray-600">Revenue (Week)</div>
        </div>
      </div>

      {loading && <p className="mt-4">Loading…</p>}
    </section>
  );
}
