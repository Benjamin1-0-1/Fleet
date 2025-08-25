import { useEffect, useState } from "react";
const KEY = "vm_dark";

export default function ThemeToggle() {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    const saved = localStorage.getItem(KEY);
    const prefers = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
    const start = saved ? saved === "1" : prefers;
    document.documentElement.classList.toggle("dark", start);
    setDark(start);
  }, []);
  const toggle = () => {
    const next = !dark; setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem(KEY, next ? "1" : "0");
  };
  return <button className="btn" onClick={toggle}>{dark ? "Light" : "Dark"}</button>;
}
