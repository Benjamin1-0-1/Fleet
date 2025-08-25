import { useState } from "react";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [err, setErr] = useState(null);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault(); setErr(null);
    try {
      const r = await api.post("/auth/login", form);
      localStorage.setItem("vm_token", r.data.access_token);
      navigate("/");
    } catch (e) {
      setErr("Invalid credentials");
    }
  };

  return (
    <div className="page">
      <form className="form" onSubmit={submit}>
        <h2>Login</h2>
        {err && <p className="text-red-600">{err}</p>}
        <label className="form__field"><span>Username</span>
          <input name="username" value={form.username} onChange={(e)=>setForm({...form,username:e.target.value})} required/>
        </label>
        <label className="form__field"><span>Password</span>
          <input type="password" name="password" value={form.password} onChange={(e)=>setForm({...form,password:e.target.value})} required/>
        </label>
        <div className="form__actions">
          <button className="btn" type="submit">Login</button>
        </div>
      </form>
    </div>
  );
}
