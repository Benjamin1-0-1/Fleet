import React, { useEffect, useState } from "react";
import { getAll, createOne, replaceOne, patchOne, deleteOne } from "../api/client";

const empty = { name: "", email: "", phone: "", address: "" };

export default function ClientsPage() {
  const [clients, setClients] = useState([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    const data = await getAll("/v1/clients");
    setClients(data.clients || []);
  };

  useEffect(() => { load(); }, []);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    if (editingId) {
      await replaceOne(`/v1/clients/${editingId}`, form);
    } else {
      await createOne("/v1/clients", form);
    }
    setForm(empty);
    setEditingId(null);
    load();
  };

  const quickEmail = async (c) => {
    const email = prompt("New email:", c.email) || c.email;
    await patchOne(`/v1/clients/${c.id}`, { email });
    load();
  };

  const remove = async (id) => { await deleteOne(`/v1/clients/${id}`); load(); };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Clients</h1>

      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-4 gap-3 bg-white p-4 rounded shadow">
        {["name","email","phone","address"].map(k => (
          <input key={k} name={k} value={form[k]} onChange={onChange} placeholder={k}
            className="border rounded px-3 py-2" />
        ))}
        <div className="md:col-span-4">
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            {editingId ? "Update Client" : "Add Client"}
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
              {["Name","Email","Phone","Address","Actions"].map(h => (
                <th key={h} className="text-left px-4 py-2">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {clients.length === 0 ? (
              <tr><td className="px-4 py-3" colSpan={5}>No clients yet.</td></tr>
            ) : clients.map(c => (
              <tr key={c.id} className="border-t">
                <td className="px-4 py-2">{c.name}</td>
                <td className="px-4 py-2">
                  {c.email}{" "}
                  <button onClick={() => quickEmail(c)} className="text-xs text-blue-600 underline ml-2">quick edit</button>
                </td>
                <td className="px-4 py-2">{c.phone}</td>
                <td className="px-4 py-2">{c.address}</td>
                <td className="px-4 py-2 space-x-2">
                  <button onClick={() => { setEditingId(c.id); setForm(c); window.scrollTo({ top: 0, behavior: "smooth" }); }} className="px-2 py-1 border rounded">Edit</button>
                  <button onClick={() => remove(c.id)} className="px-2 py-1 border rounded text-red-600">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
