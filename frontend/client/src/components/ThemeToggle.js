import { useEffect, useState } from "react";

const DARK_KEY = "vm_theme_dark";

export default function ThemeToggle() {
  const [dark, setDark] = useState(false);

  // load saved pref
  useEffect(() => {
    const saved = localStorage.getItem(DARK_KEY);
    const prefers = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
    const startDark = saved ? saved === "1" : prefers;
    if (startDark) document.documentElement.classList.add("dark");
    setDark(startDark);
  }, []);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem(DARK_KEY, next ? "1" : "0");
  };

  return (
    <button onClick={toggle} className="btn" style={{ marginLeft: 12 }}>
      {dark ? "Light Mode" : "Dark Mode"}
    </button>
  );
}
