import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/api";

export default function VehicleDetail() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    (async () => {
      const r = await api.get(`/vehicles/${id}/detail`);
      setData(r.data);
    })();
  }, [id]);

  if (!data) return <section className="page"><p>Loading…</p></section>;
  const v = data.vehicle;

  return (
    <section className="page">
      <header className="page__header"><h2>{v.plate} — {v.make} {v.model}</h2></header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card lg:col-span-1">
          {v.image_url ? <img src={v.image_url} alt={v.plate} className="w-full rounded mb-3" /> : null}
          <div className="space-y-1">
            <div><strong>Class:</strong> {v.v_class || "-"}</div>
            <div><strong>Colour:</strong> {v.colour || "-"}</div>
            <div><strong>Purchased:</strong> {v.purchase_date || "-"}</div>
            <div><strong>Purchase Price:</strong> ${Number(v.purchase_price || 0).toFixed(2)}</div>
            <div><strong>Expected Resale:</strong> ${Number(v.expected_resale || 0).toFixed(2)}</div>
            <div><strong>Odometer:</strong> {v.latest_odometer ?? "-"}</div>
          </div>
        </div>

        <div className="card lg:col-span-2">
          <h3 className="font-semibold mb-3">Financials</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 rounded bg-[color:var(--surface)] shadow"><div className="text-sm text-[color:var(--muted)]">Total Revenue</div><div className="text-2xl font-bold">${Number(data.total_revenue).toFixed(2)}</div></div>
            <div className="p-3 rounded bg-[color:var(--surface)] shadow"><div className="text-sm text-[color:var(--muted)]">Total Costs</div><div className="text-2xl font-bold">${Number(data.total_costs).toFixed(2)}</div></div>
          </div>

          <h3 className="font-semibold mt-6 mb-2">Rentals</h3>
          <table className="table">
            <thead><tr><th>ID</th><th>Client</th><th>Start</th><th>End</th><th>Returned</th><th>Rate/Day</th></tr></thead>
            <tbody>
              {data.rentals.map(r => (
                <tr key={r.id}><td>{r.id}</td><td>{r.client_id}</td><td>{r.start_date}</td><td>{r.end_date || "-"}</td><td>{r.returned_on || "-"}</td><td>${Number(r.rate_per_day).toFixed(2)}</td></tr>
              ))}
            </tbody>
          </table>

          <h3 className="font-semibold mt-6 mb-2">Damages / Changes</h3>
          <table className="table">
            <thead><tr><th>Date</th><th>Description</th><th>Cost</th></tr></thead>
            <tbody>
              {data.damages.map(d => (<tr key={d.id}><td>{d.reported_at.slice(0,10)}</td><td>{d.description}</td><td>${Number(d.cost).toFixed(2)}</td></tr>))}
              {data.damages.length === 0 && <tr><td colSpan="3">No records</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
