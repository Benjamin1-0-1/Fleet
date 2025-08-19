import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

const empty = { first_name: "", last_name: "", email: "", phone: "", address: "" };

export default function ClientForm() {
  const { id } = useParams();
  const editing = Boolean(id);
  const [form, setForm] = useState(empty);
  const navigate = useNavigate();

  useEffect(() => {
  if (!id) return;
  let alive = true;
  (async () => {
    const r = await api.get(`/clients/${id}`);
    if (alive) setForm(r.data);
  })();
  return () => { alive = false; };
}, [id]);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
  e.preventDefault();
  try {
    if (id) await api.patch(`/clients/${id}`, form);
    else await api.post(`/clients`, form);
    navigate("/clients");
  } catch (err) {
    console.error("[ClientForm] submit failed:", err);
    alert("Failed to save client.");
  }
};


  return (
    <form onSubmit={submit} className="form">
      <h2>{editing ? "Edit Client" : "Add Client"}</h2>
      {["first_name","last_name","email","phone","address"].map((name) => (
        <label key={name} className="form__field">
          <span>{name.replace("_"," ").toUpperCase()}</span>
          <input name={name} value={form[name] || ""} onChange={update} required={name!=="phone" && name!=="address"} />
        </label>
      ))}
      <div className="form__actions">
        <button type="submit" className="btn">Save</button>
        <button type="button" onClick={() => navigate("/clients")}>Cancel</button>
      </div>
    </form>
  );
}
