import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [err, setErr] = useState(null);
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault(); setErr(null);
    try {
      const r = await api.post("/auth/login", form);
      localStorage.setItem("vm_token", r.data.access_token);
      nav("/");
    } catch {
      setErr("Invalid username or password");
    }
  };

  return (
    <section className="page">
      <div className="max-w-md mx-auto card">
        <h2 className="text-xl font-semibold mb-4">Sign in</h2>
        {err && <p className="text-red-600 mb-3">{err}</p>}
        <form onSubmit={submit} className="grid gap-4">
          <label className="flex flex-col">
            <span>Username</span>
            <input value={form.username} onChange={(e)=>setForm({...form,username:e.target.value})} required />
          </label>
          <label className="flex flex-col">
            <span>Password</span>
            <input type="password" value={form.password} onChange={(e)=>setForm({...form,password:e.target.value})} required />
          </label>
          <button className="btn" type="submit">Login</button>
        </form>
        <p className="text-sm text-slate-500 mt-3">Demo: <b>admin</b> / <b>admin123</b></p>
      </div>
    </section>
  );
}
