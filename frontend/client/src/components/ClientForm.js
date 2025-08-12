import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";
import "../styles/client-form.css";

const empty = { first_name: "", last_name: "", email: "", phone: "", address: "" };

export default function ClientForm() {
  const { id } = useParams();
  const editing = Boolean(id);
  const [form, setForm] = useState(empty);
  const navigate = useNavigate();

  useEffect(() => { if (editing) api.get(`/clients/${id}`).then((r) => setForm(r.data)); }, [id]);
  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    if (editing) await api.patch(`/clients/${id}`, form);
    else await api.post(`/clients`, form);
    navigate("/clients");
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
