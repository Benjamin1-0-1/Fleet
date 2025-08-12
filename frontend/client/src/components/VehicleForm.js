import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/api";

const empty = { plate: "", make: "", model: "", v_class: "" };

export default function VehicleForm() {
  const { id } = useParams();
  const editing = Boolean(id);
  const [form, setForm] = useState(empty);
  const navigate = useNavigate();

  useEffect(() => { if (editing) api.get(`/vehicles/${id}`).then((r) => setForm(r.data)); }, [id]);

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    if (editing) await api.patch(`/vehicles/${id}`, form);
    else await api.post(`/vehicles`, form);
    navigate("/vehicles");
  };

  return (
    <form onSubmit={submit} className="form">
      <h2>{editing ? "Edit Vehicle" : "Add Vehicle"}</h2>
      {[
        ["plate","Plate"],
        ["make","Make"],
        ["model","Model"],
        ["v_class","Class"]
      ].map(([name,label]) => (
        <label key={name} className="form__field">
          <span>{label}</span>
          <input name={name} value={form[name] || ""} onChange={update} required />
        </label>
      ))}
      <div className="form__actions">
        <button type="submit" className="btn">Save</button>
        <button type="button" onClick={() => navigate("/vehicles")}>Cancel</button>
      </div>
    </form>
  );
}
