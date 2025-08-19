import { useEffect, useState } from "react";
import api from "../api/api";
import ReminderList from "../components/ReminderList";
import ReminderForm from "../components/ReminderForm";

export default function RemindersPage() {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = async () => {
    try {
      const r = await api.get("/reminders");
      setReminders(r.data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to fetch reminders");
      console.error("[RemindersPage] load failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const r = await api.get("/reminders");
        if (alive) {
          setReminders(r.data);
          setError(null);
        }
      } catch (err) {
        if (alive) setError(err.message || "Failed to fetch reminders");
        console.error("[RemindersPage] initial load failed:", err);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  if (loading) return <section className="page"><p>Loading reminders...</p></section>;
  if (error) return <section className="page"><p className="error">{error}</p></section>;

  return (
    <section className="page">
      <header className="page__header"><h2>Reminders</h2></header>
      <ReminderForm onSaved={refresh} />
      <ReminderList items={reminders} onChanged={refresh} />
    </section>
  );
}
