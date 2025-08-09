import React, { useEffect, useState } from "react";
import { getAll, createOne, replaceOne, patchOne, deleteOne } from "../api/client";

const empty = { vehicle_id: "", remind_at: "", type: "", note: "" };

export default function RemindersPage() {
  const [reminders, setReminders] = useState([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    const data = await getAll("/v1/reminders");
    setReminders(data.reminders || []);
  };

  useEffect(() => { load(); }, []);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const payload = { ...form, vehicle_id: parseInt(form.vehicle_id, 10) };
    if (editingId) {
      await replaceOne(`/v1/reminders/${editingId}`, payload);
    } else {
      await createOne("/v1/reminders", payload);
    }
    setForm(empty);
    setEditingId(null);
    load();
  };

  const quickNote = async (r) => {
    const note = prompt("New note:", r.note || "") ?? r.note;
    await patchOne(`/v1/reminders/${r.id}`, { note });
    load();
  };

  const remove = async (id) => { await deleteOne(`/v1/reminders/${id}`); load(); };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Reminders</h1>

      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-4 gap-3 bg-white p-4 rounded shadow">
        <input name="vehicle_id" value={form.vehicle_id} onChange={onChange} placeholder="vehicle_id" className="border rounded px-3 py-2" />
        <input name="remind_at" value={form.remind_at} onChange={onChange} placeholder="YYYY-MM-DDTHH:MM:SS" className="border rounded px-3 py-2" />
        <input name="type" value={form.type} onChange={onChange} placeholder="type" className="border rounded px-3 py-2" />
        <input name="note" value={form.note} onChange={onChange} placeholder="note" className="border rounded px-3 py-2" />
        <div className="md:col-span-4">
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            {editingId ? "Update Reminder" : "Add Reminder"}
          </button>
          {editingId && (
            <button type="button" className="ml-3 px-4 py-2 rounded border"
              onClick={() => { setEditingId(null); setForm(empty); }}>
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              {["Vehicle","Remind At","Type","Note","Actions"].map(h => (
                <th key={h} className="text-left px-4 py-2">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {reminders.length === 0 ? (
              <tr><td className="px-4 py-3" colSpan={5}>No reminders yet.</td></tr>
            ) : reminders.map(r => (
              <tr key={r.id} className="border-t">
                <td className="px-4 py-2">{r.vehicle_id}</td>
                <td className="px-4 py-2">{r.remind_at}</td>
                <td className="px-4 py-2">{r.type || "-"}</td>
                <td className="px-4 py-2">{r.note || "-"}</td>
                <td className="px-4 py-2 space-x-2">
                  <button onClick={() => { setEditingId(r.id); setForm({ vehicle_id: r.vehicle_id, remind_at: r.remind_at, type: r.type || "", note: r.note || "" }); window.scrollTo({ top: 0, behavior: "smooth" }); }} className="px-2 py-1 border rounded">Edit</button>
                  <button onClick={() => quickNote(r)} className="px-2 py-1 border rounded">Quick Note</button>
                  <button onClick={() => remove(r.id)} className="px-2 py-1 border rounded text-red-600">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
