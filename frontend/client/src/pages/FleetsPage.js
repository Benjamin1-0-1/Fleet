import React, { useEffect, useState } from "react";
import { getAll, createOne, replaceOne, patchOne, deleteOne } from "../api/client";

const empty = {
  plate: "", make: "", color: "",
  classification: "",
  purchase_price: "", expected_resale: ""
};

export default function FleetsPage() {
  const [fleets, setFleets] = useState([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    const data = await getAll("/v1/fleets");
    setFleets(data.fleets || []);
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const payload = {
      ...form,
      purchase_price: form.purchase_price ? parseFloat(form.purchase_price) : undefined,
      expected_resale: form.expected_resale ? parseFloat(form.expected_resale) : undefined
    };
    if (editingId) {
      await replaceOne(`/v1/fleets/${editingId}`, payload);
    } else {
      await createOne("/v1/fleets", payload);
    }
    setForm(empty);
    setEditingId(null);
    load();
  };

  const startEdit = (v) => {
    setEditingId(v.id);
    setForm({
      plate: v.plate || "",
      make: v.make || "",
      color: v.color || "",
      classification: v.classification || "",
      purchase_price: v.purchase_price ?? "",
      expected_resale: v.expected_resale ?? ""
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const partialUpdateColor = async (id, color) => {
    await patchOne(`/v1/fleets/${id}`, { color });
    load();
  };

  const remove = async (id) => {
    await deleteOne(`/v1/fleets/${id}`);
    load();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Fleets</h1>

      {/* Create / Edit form */}
      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-white p-4 rounded shadow">
        {["plate","make","color","classification","purchase_price","expected_resale"].map((k) => (
          <input
            key={k}
            name={k}
            value={form[k]}
            onChange={onChange}
            placeholder={k.replace("_", " ")}
            className="border rounded px-3 py-2"
          />
        ))}
        <div className="md:col-span-3">
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            {editingId ? "Update Vehicle" : "Add Vehicle"}
          </button>
          {editingId && (
            <button
              type="button"
              onClick={() => { setEditingId(null); setForm(empty); }}
              className="ml-3 px-4 py-2 rounded border"
            >
              Cancel
            </button>
          )}
        </div>
      </form>

      {/* List */}
      <div className="bg-white rounded shadow overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              {["Plate","Make","Color","Class","Purchase","Resale","Actions"].map(h => (
                <th key={h} className="text-left px-4 py-2">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td className="px-4 py-3" colSpan={7}>Loading…</td></tr>
            ) : fleets.length === 0 ? (
              <tr><td className="px-4 py-3" colSpan={7}>No vehicles yet.</td></tr>
            ) : fleets.map(v => (
              <tr key={v.id} className="border-t">
                <td className="px-4 py-2">{v.plate}</td>
                <td className="px-4 py-2">{v.make}</td>
                <td className="px-4 py-2">
                  {v.color}{" "}
                  <button
                    onClick={() => partialUpdateColor(v.id, prompt("New color:", v.color) || v.color)}
                    className="text-xs text-blue-600 underline ml-2"
                  >
                    quick edit
                  </button>
                </td>
                <td className="px-4 py-2">{v.classification}</td>
                <td className="px-4 py-2">{v.purchase_price ?? "-"}</td>
                <td className="px-4 py-2">{v.expected_resale ?? "-"}</td>
                <td className="px-4 py-2 space-x-2">
                  <button onClick={() => startEdit(v)} className="px-2 py-1 border rounded">Edit</button>
                  <button onClick={() => remove(v.id)} className="px-2 py-1 border rounded text-red-600">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
