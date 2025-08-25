import { useEffect, useState } from "react";
import api from "../api/api";

export default function RemindersPage() {
  const [saved, setSaved] = useState([]);
  const [generated, setGenerated] = useState({ overdue: [], fuel: [] });

  const refresh = async () => {
    const r = await api.get("/reminders/all");
    setSaved(r.data.saved); setGenerated(r.data.generated);
  };

  useEffect(() => { refresh(); }, []);

  const section = (title, items) => (
    <div className="card">
      <h3 className="font-semibold mb-2">{title}</h3>
      <table className="table">
        <thead><tr><th>Vehicle</th><th>Type</th><th>Due</th></tr></thead>
        <tbody>
          {items.map((x,i) => (<tr key={x.id || i}><td>{x.vehicle_id}</td><td>{x.reminder_type}</td><td>{x.due_date}</td></tr>))}
          {items.length===0 && <tr><td colSpan="3">None</td></tr>}
        </tbody>
      </table>
    </div>
  );

  return (
    <section className="page">
      <header className="page__header"><h2>Reminders</h2></header>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {section("Saved", saved)}
        {section("Overdue Rentals (auto)", generated.overdue)}
        {section("Fuel Needed (auto)", generated.fuel)}
      </div>
    </section>
  );
}
