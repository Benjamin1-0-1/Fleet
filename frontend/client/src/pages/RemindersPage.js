import { useEffect, useState } from "react";
import api from "../api/api";

export default function RemindersPage() {
  const [saved, setSaved] = useState([]);
  const [generated, setGenerated] = useState({ overdue: [], fuel: [] });
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = async () => {
    setLoading(true);
    setErr(null);
    try {
      const r = await api.get("/reminders/all"); // -> /api/reminders/all
      const data = r.data || {};
      // Accept either the nested 'generated' shape or the flat keys
      const gen = data.generated || {
        overdue: data.overdue_rentals || [],
        fuel: data.fuel_needed || [],
      };
      setSaved(data.saved || []);
      setGenerated({ overdue: gen.overdue || [], fuel: gen.fuel || [] });
    } catch (e) {
      console.error("[Reminders] load failed:", e);
      setErr("Failed to load reminders.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let alive = true;
    (async () => {
      try { await refresh(); } catch {}
    })();
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const section = (title, items) => (
    <div className="card">
      <h3 className="font-semibold mb-2">{title}</h3>
      <table className="table">
        <thead>
          <tr><th>Vehicle</th><th>Type</th><th>Due</th></tr>
        </thead>
        <tbody>
          {items.map((x, i) => (
            <tr key={x.id ?? `${title}-${i}`}>
              <td>{x.vehicle_id ?? "-"}</td>
              <td>{x.reminder_type ?? "-"}</td>
              <td>{x.due_date ?? (x.level !== undefined ? `${x.level}%` : "-")}</td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr><td colSpan="3">None</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );

  return (
    <section className="page">
      <header className="page__header">
        <h2>Reminders</h2>
        <button className="btn-outline" onClick={refresh} disabled={loading}>
          {loading ? "Loading..." : "Refresh"}
        </button>
      </header>

      {err && <p className="text-red-600 mb-3">{err}</p>}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {section("Saved", saved)}
        {section("Overdue Rentals (auto)", generated.overdue)}
        {section("Fuel Needed (auto)", generated.fuel)}
      </div>
    </section>
  );
}
