import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

const EMPTY = { plate:"", make:"", model:"", v_class:"", colour:"", purchase_price:"" };

export default function VehicleForm() {
  const { id } = useParams();
  const editing = !!id && id !== "new"; // ✅ never treat “new” as an id
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const nav = useNavigate();

  useEffect(() => {
    if (!editing) return;
    let alive = true;
    (async () => {
      const r = await api.get(`/vehicles/${id}`);
      if (alive) setForm({
        plate: r.data.plate || "",
        make: r.data.make || "",
        model: r.data.model || "",
        v_class: r.data.v_class || "",
        colour: r.data.colour || "",
        purchase_price: r.data.purchase_price || ""
      });
    })();
    return () => { alive = false; };
  }, [editing, id]);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      if (editing) await api.patch(`/vehicles/${id}`, form);
      else await api.post(`/vehicles`, form);
      nav("/vehicles");
    } catch (e) {
      alert("Failed to save vehicle. Check backend logs.");
      console.error(e);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="page">
      <header className="page__header">
        <h2>{editing ? "Edit Vehicle" : "Add Vehicle"}</h2>
      </header>
      <form onSubmit={submit} className="card grid gap-4 md:grid-cols-2">
        <label className="flex flex-col">
          <span>Plate</span>
          <input value={form.plate} onChange={(e)=>setForm({...form, plate:e.target.value})} required />
        </label>
        <label className="flex flex-col">
          <span>Make</span>
          <input value={form.make} onChange={(e)=>setForm({...form, make:e.target.value})} required />
        </label>
        <label className="flex flex-col">
          <span>Model</span>
          <input value={form.model} onChange={(e)=>setForm({...form, model:e.target.value})} required />
        </label>
        <label className="flex flex-col">
          <span>Class</span>
          <input value={form.v_class} onChange={(e)=>setForm({...form, v_class:e.target.value})} />
        </label>
        <label className="flex flex-col">
          <span>Colour</span>
          <input value={form.colour} onChange={(e)=>setForm({...form, colour:e.target.value})} />
        </label>
        <label className="flex flex-col">
          <span>Purchase Price</span>
          <input type="number" step="0.01" value={form.purchase_price}
                 onChange={(e)=>setForm({...form, purchase_price:e.target.value})} />
        </label>

        <div className="md:col-span-2 flex gap-3">
          <button className="btn" disabled={busy} type="submit">{busy ? "Saving..." : "Save"}</button>
          <button className="btn-outline" type="button" onClick={()=>nav("/vehicles")}>Cancel</button>
        </div>
      </form>
    </section>
  );
}
