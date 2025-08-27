import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

const EMPTY = { first_name:"", last_name:"", email:"", phone:"", address:"" };

export default function ClientForm() {
  const { id } = useParams();
  const editing = !!id && id !== "new";
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const nav = useNavigate();

  useEffect(() => {
    if (!editing) return;
    let alive = true;
    (async () => {
      const r = await api.get(`/clients/${id}`);
      if (alive) setForm({
        first_name: r.data.first_name || "",
        last_name:  r.data.last_name  || "",
        email:      r.data.email      || "",
        phone:      r.data.phone      || "",
        address:    r.data.address    || ""
      });
    })();
    return () => { alive = false; };
  }, [editing, id]);

  const submit = async (e) => {
    e.preventDefault(); setBusy(true);
    try {
      if (editing) await api.patch(`/clients/${id}`, form);
      else await api.post(`/clients`, form);
      nav("/clients");
    } catch (e) {
      console.error(e); alert("Failed to save client.");
    } finally { setBusy(false); }
  };

  return (
    <section className="page">
      <header className="page__header"><h2>{editing ? "Edit Client" : "Add Client"}</h2></header>
      <form onSubmit={submit} className="card grid gap-4 md:grid-cols-2">
        <label className="flex flex-col"><span>First name</span>
          <input value={form.first_name} onChange={(e)=>setForm({...form, first_name:e.target.value})} required />
        </label>
        <label className="flex flex-col"><span>Last name</span>
          <input value={form.last_name} onChange={(e)=>setForm({...form, last_name:e.target.value})} required />
        </label>
        <label className="flex flex-col md:col-span-2"><span>Email</span>
          <input type="email" value={form.email} onChange={(e)=>setForm({...form, email:e.target.value})} required />
        </label>
        <label className="flex flex-col"><span>Phone</span>
          <input value={form.phone} onChange={(e)=>setForm({...form, phone:e.target.value})} />
        </label>
        <label className="flex flex-col md:col-span-2"><span>Address</span>
          <input value={form.address} onChange={(e)=>setForm({...form, address:e.target.value})} />
        </label>
        <div className="md:col-span-2 flex gap-3">
          <button className="btn" disabled={busy} type="submit">{busy ? "Saving..." : "Save"}</button>
          <button className="btn-outline" type="button" onClick={()=>nav("/clients")}>Cancel</button>
        </div>
      </form>
    </section>
  );
}
