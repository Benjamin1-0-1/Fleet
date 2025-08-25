import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/api";
import { Bar, Line } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from "chart.js";
ChartJS.register(BarElement, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function Dashboard() {
  const [summary, setSummary] = useState({ vehicles: 0, total_costs: 0, revenue_week: 0, revenue_month: 0, revenue_year: 0 });
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const s = await api.get("/analytics/summary"); setSummary(s.data);
        const v = await api.get("/vehicles"); setVehicles(v.data);
      } catch (e) { console.error(e); }
    })();
  }, []);

  const revenueData = {
    labels: ["This Week", "This Month", "This Year"],
    datasets: [{ label: "Revenue", data: [summary.revenue_week, summary.revenue_month, summary.revenue_year] }]
  };

  const vehicleTable = (
    <table className="table">
      <thead><tr><th>Image</th><th>Plate</th><th>Make/Model</th><th>Class</th><th>Odometer</th><th>Status</th></tr></thead>
      <tbody>
        {vehicles.map(v => (
          <tr key={v.id}>
            <td>{v.image_url ? <img src={v.image_url} alt={v.plate} style={{width:64,height:40,objectFit:"cover"}}/> : "—"}</td>
            <td><Link to={`/vehicles/${v.id}`}>{v.plate}</Link></td>
            <td>{v.make} {v.model}</td>
            <td>{v.v_class || "-"}</td>
            <td>{v.latest_odometer ?? "-"}</td>
            <td>{v.active_client_id ? "On Rent" : "Available"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <section className="page">
      <header className="page__header"><h2>Dashboard</h2></header>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="stat card text-center"><div className="text-3xl font-bold">{summary.vehicles}</div><div>Vehicles</div></div>
        <div className="stat card text-center"><div className="text-3xl font-bold">${Number(summary.total_costs).toFixed(2)}</div><div>Total Costs</div></div>
        <div className="stat card text-center"><div className="text-3xl font-bold">${Number(summary.revenue_month).toFixed(2)}</div><div>Revenue (Month)</div></div>
        <div className="stat card text-center"><div className="text-3xl font-bold">${Number(summary.revenue_week).toFixed(2)}</div><div>Revenue (Week)</div></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="card"><h3 className="font-semibold mb-4">Revenue Overview</h3><Bar data={revenueData} /></div>
        <div className="card"><h3 className="font-semibold mb-4">Maintenance Trend</h3>
          <Line data={{ labels: ["Jan","Feb","Mar","Apr","May","Jun"], datasets:[{ label:"Costs", data:[200,320,150,480,260,390]}] }} />
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-4">Fleet Snapshot</h3>
        {vehicleTable}
      </div>
    </section>
  );
}
