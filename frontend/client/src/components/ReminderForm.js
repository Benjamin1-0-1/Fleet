import { useEffect, useState } from "react";
import api from "../api/api";

export default function ReminderForm({ onSaved }) {
  const [vehicles, setVehicles] = useState([]);
  const [form, setForm] = useState({ vehicle_id: "", reminder_type: "service", due_date: "" });

  useEffect(() => { api.get("/vehicles").then((r) => setVehicles(r.data)); }, []);
  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
  e.preventDefault();
  try {
    await api.post("/reminders", {
      ...form,
      vehicle_id: Number(form.vehicle_id) || undefined
    });
    setForm({ vehicle_id: "", reminder_type: "service", due_date: "" });
    onSaved?.();
  } catch (err) {
    console.error("[ReminderForm] submit failed:", err);
    alert("Failed to add reminder.");
  }
};


  return (
    <form className="form" onSubmit={submit}>
      <h3>New Reminder</h3>
      <label className="form__field">
        <span>Vehicle</span>
        <select name="vehicle_id" value={form.vehicle_id} onChange={update} required>
          <option value="" disabled>Select a vehicle</option>
          {vehicles.map((v) => (
            <option key={v.id} value={v.id}>{v.plate} — {v.make}</option>
          ))}
        </select>
      </label>
      <label className="form__field">
        <span>Type</span>
        <select name="reminder_type" value={form.reminder_type} onChange={update}>
          <option value="service">service</option>
          <option value="return">return</option>
          <option value="insurance">insurance</option>
        </select>
      </label>
      <label className="form__field">
        <span>Due Date</span>
        <input type="date" name="due_date" value={form.due_date} onChange={update} required />
      </label>
      <div className="form__actions">
        <button className="btn" type="submit">Add</button>
      </div>
    </form>
  );
}
